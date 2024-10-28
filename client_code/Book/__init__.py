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

    stuff = anvil.server.call('get_all_jugendherberge')
    print(stuff)


  def link_home_click(self, **event_args):
    open_form('Home')
    pass

  def link_book_click(self, **event_args):
    open_form('Book')
    pass

  def link_statistics_click(self, **event_args):
    open_form('Statistics')
    pass

  
  
  

 