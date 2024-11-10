import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3, re
from passlib.hash import sha256_crypt
import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
db_path=data_files["database.db"]

def hash_password(password: str) -> str:
  return sha256_crypt.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
  return sha256_crypt.verify(password, hashed_password)

@anvil.server.callable
def get_user_id():
  userId = anvil.server.session.get('userId', None)
  return userId
  
@anvil.server.callable
def login(username, password):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("SELECT UID, Username, Password  FROM User WHERE Username = ?", (username,))
  user = cursor.fetchone()
  
  if user is not None:
    if verify_password(password, user[2]):
      userId = anvil.server.session.get("userId", None)
      userId = user[0]
    
      anvil.server.session["userId"] = userId
      
      connection.close()
      return True, "Successfully logged in"


  connection.close()
  return False, "Username or password is incorrect"

@anvil.server.callable
def register(username, password):

  if len(username) > 50 and len(username) < 3:
    return False, "Username has to be between 3 and 50 characters"

  if len(password) < 8:
    return False, "Passowrd has to be at least 8 characters"

  if not re.match("^[A-Za-z0-9_]+$", username):
    return False, "Username can only contain letters, numbers, and underscores, with no spaces."
  
  password = hash_password(password)
  
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("SELECT Username FROM User WHERE Username = ?", (username,))
  user = cursor.fetchone()
  
  if user is None:
    cursor.execute("INSERT INTO User (PID, Username, Password) VALUES (?, ?, ?);", (1, username, password))
    userId = cursor.lastrowid
    anvil.server.session["userId"] = userId
    connection.commit()
    
    connection.close()
    return True, "Account successfully created"
  
  connection.close()
  return False, "Username already taken"

@anvil.server.callable
def logout():
  anvil.server.session["userId"] = None
  return True

@anvil.server.callable
def change_password(current, new):
  print(current, new)
  # Ensure the user is logged in
  userId = get_user_id()
  if userId is None:
    return False, "You must be logged in to change your password."

  if len(new) < 8:
    return False, "New passowrd has to be at least 8 characters"
  
  # Connect to the database
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  # Get the current user's data
  cursor.execute("SELECT Password FROM User WHERE UID = ?", (userId,))
  user = cursor.fetchone()
  
  if user is None:
    connection.close()
    return False, "User not found."

  # Verify the old password
  if not verify_password(current, user[0]):
    connection.close()
    return False, "Incorrect old password."

  # Hash the new password
  new_password_hashed = hash_password(new)

  # Update the password in the database
  cursor.execute("UPDATE User SET Password = ? WHERE UID = ?", (new_password_hashed, userId))
  connection.commit()
  
  connection.close()
  
  return True, "Password successfully changed."

@anvil.server.callable
def get_all_jugendherberge():
  # Connect to the SQLite database
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  
  # Execute the query to get all Jugendherberge data
  cursor.execute("SELECT JID, Name, Address FROM Jugendherberge;")
  jugendherberge_data = cursor.fetchall()
  
  # Close the connection
  connection.close()
  
  return jugendherberge_data

@anvil.server.callable
def get_rooms_by_jugendherberge(jugendherberge_id):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("""
      SELECT Room.RoomNr, Room.Beds, PriceCategory.Name AS PriceCategoryName, Room.RID
      FROM Room
      JOIN PriceCategory ON Room.PID = PriceCategory.PID
      WHERE Room.JID = ?;
  """, (jugendherberge_id,))
  
  rooms = cursor.fetchall()

  connection.close()
  
  return rooms
    

@anvil.server.callable
def get_bookings_by_user():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    userId = get_user_id()
  
    cursor.execute("""
    SELECT 
        Room.RoomNr AS roomNr,
        book.Startdate AS startdate,
        book.Enddate AS enddate,
        Room.Beds AS countBeds,
        PriceCategory.Name AS priceCategoryName,
        Jugendherberge.Address AS location,
        book.price
    FROM 
        book
    JOIN
        Room ON book.RID = Room.RID
    JOIN 
        PriceCategory ON Room.PID = PriceCategory.PID
    JOIN 
        Jugendherberge ON Room.JID = Jugendherberge.JID
    LEFT JOIN 
        bookWith ON book.BID = bookWith.BID
    WHERE
        book.UID = ? OR bookWith.UID = ?;
    """, (userId, userId))
  
    bookings = cursor.fetchall()
    connection.close()
    return bookings

def add_username_to_booking(cursor, username, BID):
  cursor.execute("SELECT UID FROM User WHERE Username = ?", (username,))
  userId = cursor.fetchone()
    
  if userId:
    UID = userId[0]
    cursor.execute("INSERT INTO bookWith (BID, UID) VALUES (?, ?)", (BID, UID))
    #print(f"User '{username}' linked to booking ID {BID}")
  #else:
    #print(f"Username '{username}' does not exist.")

@anvil.server.callable
def save_booking(RID, room_nr, start_date, end_date, price, addedUsers):
  connection = None

  #print(addedUsers)
  
  try:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    userId = get_user_id()
    
    parameters = (start_date, end_date, price, userId, RID)
    insert_query = """
    INSERT INTO book (Startdate, Enddate, price, UID, RID)
    VALUES (?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_query, parameters)

    BID = cursor.lastrowid
    for username in addedUsers:
      add_username_to_booking(cursor, username, BID)
  
    connection.commit()
    #print("Buchung erfolgreich gespeichert.")
    
  except sqlite3.Error as e:
    print(f"Fehler beim Speichern der Buchung: {e}")
    raise RuntimeError("Fehler beim Speichern der Buchung.")
    
  finally:
    if connection:
      connection.close()

@anvil.server.callable
def get_all_users(withoutSelf = False):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  userId = get_user_id()

  if withoutSelf:
    cursor.execute("SELECT Username FROM User WHERE NOT UID = ?", (userId,))
  else:
    cursor.execute("SELECT Username FROM User")
  users = cursor.fetchall()
  
  connection.close()
  return [user[0] for user in users]



@anvil.server.callable
def get_price_per_night(priceCategory, beds):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("SELECT CostPerNight FROM PriceCategory WHERE Name = ?", (priceCategory,))
  row = cursor.fetchone()

  if row:
    base_price = row[0]

  connection.close()

  price = base_price + (beds * 10)
  return price


@anvil.server.callable
def is_room_available(RID, start_date, end_date):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1 FROM book
        WHERE RID = ?
        AND NOT (Enddate < ? OR Startdate > ?)
    """, (RID, start_date, end_date))

    available = cursor.fetchone() is None

    connection.close()
    return available

@anvil.server.callable
def get_unavailable_dates(RID, start_date, end_date):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Startdate, Enddate FROM book
        WHERE RID = ?
        AND NOT (Enddate < ? OR Startdate > ?)
    """, (RID, start_date, end_date))

    unavailable_dates = cursor.fetchall()

    connection.close()

    return unavailable_dates


@anvil.server.callable
def get_username():
  userId = get_user_id()
  if userId is None:
    return None

  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("SELECT Username FROM User WHERE UID = ?", (userId,))
  result = cursor.fetchone()
  
  connection.close()
  
  if result:
    return result[0]
  else:
    return None
  
@anvil.server.callable
def save_profile_picture(profile_picture_file):
    user_id = get_user_id()
    if user_id:
      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()

      profile_picture_blob = profile_picture_file.get_bytes() if profile_picture_file else None
      
      if profile_picture_blob is None:
        profile_picture_blob = get_default_profile_picture()

      cursor.execute("UPDATE User SET ProfilePicture = ? WHERE UID = ?", (profile_picture_blob, user_id))
      connection.commit()
      connection.close()


@anvil.server.callable
def get_profile_picture():
    user_id = get_user_id()
    if user_id:
      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()

      cursor.execute("SELECT ProfilePicture FROM User WHERE UID = ?", (user_id,))
      result = cursor.fetchone()
      connection.close()

      if result and result[0]:
        return anvil.BlobMedia("image/png", result[0])
      else:
        return get_default_profile_picture()

    return get_default_profile_picture()

@anvil.server.callable
def get_default_profile_picture():
  user_image = data_files['user.png']
  return anvil.BlobMedia("image/png", user_image)