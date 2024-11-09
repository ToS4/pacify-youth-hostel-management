from ._anvil_designer import BookTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Book(BookTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    data_all_jugendherberge = anvil.server.call('get_all_jugendherberge')
    #print(data_all_jugendherberge)

    jugendherberge = []
    for row in data_all_jugendherberge:
        jugendherberge.append((row[2], row))  

    self.drop_down_location.items = jugendherberge  
    #self.drop_down_location.selected_value = None  
    self.update_rooms()

    self.check_login()

    """profile_picture = anvil.server.call('get_profile_picture')
    if profile_picture:
      self.image_profilepicture.source = profile_picture
    else:
      self.image_profilepicture.source = anvil.server.call('get_default_profile_picture')"""

    
  def check_login(self):
    userId = anvil.server.call('get_user_id')
    if userId is None:
      self.button_login_logout.text = "Login / Register"
      #self.image_profilepicture.source = anvil.server.call('get_default_profile_picture')
    else:
      self.button_login_logout.text = "Logout"

  def update_rooms(self):
    selected_value = self.drop_down_location.selected_value

    if selected_value is None:
        #print("Kein Wert im Dropdown ausgewählt.")
        return

    jugendherberge_id = selected_value[0] 
    #print(f"Ausgewählte Jugendherberge ID: {jugendherberge_id}")

    try:
        data_rooms_by_jugendherberge = anvil.server.call('get_rooms_by_jugendherberge', jugendherberge_id)
        #print(f"Daten der Räume: {data_rooms_by_jugendherberge}")

        #if not data_rooms_by_jugendherberge:
            #print("Keine Räume für diese Jugendherberge gefunden!")

        rooms_by_jugendherberge = []

        for row in data_rooms_by_jugendherberge:
            toAdd = {
                'roomNr': row[0],
                'countBeds': row[1],
                'priceCategory': row[2],
                'RID': row[3]
            }
            rooms_by_jugendherberge.append(toAdd)

        #if not rooms_by_jugendherberge:
            #print("Keine Zimmer zum Anzeigen.")
        
        self.repeating_panel_rooms.items = rooms_by_jugendherberge
        #print(f"Zimmer angezeigt: {rooms_by_jugendherberge}")

    except Exception as e:
        print(f"Fehler beim Abrufen der Räume: {e}")

  def link_home_click(self, **event_args):
    open_form('Home')

  def link_book_click(self, **event_args):
    open_form('Book')

  def link_statistics_click(self, **event_args):
    open_form('Statistics')

  def button_login_register_click(self, **event_args):
    userId = anvil.server.call('get_user_id')
    if userId is None:
      open_form('Home')
    else:
      anvil.server.call('logout')
    open_form('Home')

  def drop_down_location_change(self, **event_args):
    #print(f"Dropdown geändert: {self.drop_down_location.selected_value}")
    self.update_rooms()

  def link_settings_click(self, **event_args):
    open_form('Settings')
    

