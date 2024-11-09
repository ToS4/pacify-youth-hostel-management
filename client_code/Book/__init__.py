from ._anvil_designer import BookTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Book(BookTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    data_all_jugendherberge = anvil.server.call('get_all_jugendherberge')
    print(data_all_jugendherberge)

    jugendherberge = []
    for row in data_all_jugendherberge:
        jugendherberge.append((row[2], row))
    
    self.drop_down_location.items = jugendherberge

    self.update_rooms()
    self.check_login()

  def check_login(self):
    userId = anvil.server.call('get_user_id')
    print(userId)
    if userId is None:
      self.button_login_logout.text = "Login / Register"
      open_form('LoginRegister')
    else:
      self.button_login_logout.text = "Logout"
  
  
  def update_rooms(self):
      selected_value = self.drop_down_location.selected_value
      print(selected_value)
  
      data_rooms_by_jugendherberge = anvil.server.call('get_rooms_by_jugendherberge', selected_value[0])
      print(data_rooms_by_jugendherberge)
      
      rooms_by_jugendherberge = []
      for row in data_rooms_by_jugendherberge:
          toAdd = {
              'roomNr': row[0],        
              'countBeds': row[1],
              'priceCategory': row[2]
          }
          rooms_by_jugendherberge.append(toAdd)
  
      self.repeating_panel_rooms.items = rooms_by_jugendherberge

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
      

