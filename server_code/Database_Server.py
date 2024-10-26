import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

@anvil.server.callable
def get_all_jugendherberge():
  db_path="database.db"
  
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
  db_path="database.db"

  # Connect to the SQLite database
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()

  # Execute the query to get all rooms for the specified Jugendherberge ID
  cursor.execute("SELECT RID, Beds, PID FROM Room WHERE JID = ?;", (jugendherberge_id,))
  rooms = cursor.fetchall()

  # Close the connection
  connection.close()
  
  return rooms