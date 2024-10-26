from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from ..Statistics import Statistics
from ..Book import Book

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def link_home_click(self, **event_args):
    pass

  def link_statistics_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Statistics())
    pass

  def link_book_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Book())
    pass

  def button_login_register_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
