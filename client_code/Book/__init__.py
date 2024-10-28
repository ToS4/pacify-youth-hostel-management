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
  

  def update_rooms(self):
    selected_value = self.drop_down_location.selected_value
    print(selected_value)

    data_rooms_by_jugendherberge = anvil.server.call('get_rooms_by_jugendherberge', selected_value[0])
    print(data_rooms_by_jugendherberge)
    
    rooms_by_jugendherberge = []
    for row in data_rooms_by_jugendherberge:
      toAdd = {'roomNr': row[0], 'countBeds': row[1], 'priceCategory': row[2]}
      rooms_by_jugendherberge.append(toAdd)

    self.repeating_panel_rooms.items = rooms_by_jugendherberge
    
  
  def link_home_click(self, **event_args):
    open_form('Home')

  def link_book_click(self, **event_args):
    open_form('Book')

  def link_statistics_click(self, **event_args):
    open_form('Statistics')

  def drop_down_location_change(self, **event_args):
    """This method is called when an item is selected"""
    self.update_rooms()

  
  
  

 