from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    jugendherbergen = anvil.server.call("get_jugendherbergen")
    item_list = []
    for row in jugendherbergen:
        item_list.append((row[1], row))
    self.drop_down_1.items = item_list
  
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
