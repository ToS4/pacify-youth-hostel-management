from ._anvil_designer import BookTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

"""from ..Home import Home
from ..Statistics import Statistics"""

class Book(BookTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
"""
  def link_home_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    pass

  def link_book_click(self, **event_args):
    pass

  def link_statistics_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Statistics())
    pass"""

  
  
  

 