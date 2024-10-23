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
def get_jugendherbergen():
  conn = sqlite3.connect(data_files['jugendherberge.db'])
  cursor = conn.cursor()
  
  results = list(cursor.execute('SELECT Name, ID FROM Jugendherberge'))
  
  print("Server", results)

  print("Hallo")
  
  conn.commit()
  conn.close()

  return results

@anvil.server.callable
def get_zimmerDaten():
  conn = sqlite3.connect(data_files['jugendherberge.db'])
  cursor = conn.cursor()
  
  results = list(cursor.execute('''SELECT 
      Zimmer.MaxPersonen,
      Jugendherberge.ID AS Jugendherberge_ID,
      Preiskategorie.Titel AS Preiskategorie_Titel
  FROM 
      Zimmer
  JOIN 
      ZimmerJugendherberge ON Zimmer.ID = ZimmerJugendherberge.ZimmerID
  JOIN 
      Jugendherberge ON ZimmerJugendherberge.JugendherbergeID = Jugendherberge.ID
  JOIN 
      ZimmerPreiskategorie ON Zimmer.ID = ZimmerPreiskategorie.ZimmerID
  JOIN 
      Preiskategorie ON ZimmerPreiskategorie.PreiskategorieID = Preiskategorie.ID
  '''))

 print("Server", results)
  
  conn.commit()
  conn.close()

  return results


def asdasd():
  