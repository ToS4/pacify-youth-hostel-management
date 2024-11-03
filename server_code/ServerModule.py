import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
from passlib.hash import sha256_crypt

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

  cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
  user = cursor.fetchone()
  
  if user is not None:
    if verify_password(password, user[3]):
      userId = anvil.server.session.get("userId", None)
      userId = user[0]
    
      anvil.server.session["userId"] = userId
      
      connection.close()
      return True, "Successfully logged in"


  connection.close()
  return False, "Username or password is incorrect"

@anvil.server.callable
def register(username, password):
  password = hash_password(password)
  
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
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
        SELECT Room.RoomNr, Room.Beds, PriceCategory.Name AS PriceCategoryName
        FROM Room
        JOIN PriceCategory ON Room.PID = PriceCategory.PID
        WHERE Room.JID = ?;
    """, (jugendherberge_id,))
  
    rooms = cursor.fetchall()

    # Close the connection
    connection.close()
  
    return rooms


@anvil.server.callable
def get_bookings_by_user(user_id):
  # Connect to the SQLite database
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  cursor.execute("""
        SELECT 
            Room.RID AS RoomRID, 
            book.Startdate, 
            book.Enddate, 
            Room.Beds AS RoomBeds, 
            PriceCategory.Name AS PriceCategoryName,
            Jugendherberge.Address AS JugendherbergeAddress
        FROM 
            book
        JOIN 
            Room ON book.RID = Room.RID
        JOIN 
            PriceCategory ON Room.PID = PriceCategory.PID
        JOIN 
            Jugendherberge ON Room.JID = Jugendherberge.JID
        WHERE 
            book.UID = ?;
    """, (user_id,))
  
  bookings = cursor.fetchall()

  # Close the connection
  connection.close()
  return bookings


@anvil.server.callable
def save_booking(room_nr, start_date, end_date, price):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO book (RoomNr, Startdate, Enddate, price)
        VALUES (?, ?, ?, ?)
        """

        parameters = (room_nr, start_date, end_date, price)

        cursor.execute(insert_query, parameters)
        connection.commit()
        print("Buchung erfolgreich gespeichert.")

    except sqlite3.Error as e:
        print(f"Fehler beim Speichern der Buchung: {e}")
        raise RuntimeError("Fehler beim Speichern der Buchung.")
        
    finally:
        if connection:
            connection.close()