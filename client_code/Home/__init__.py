from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    jugendherbergen = anvil.server.call("get_jugendherbergen")
    self.drop_down_1.items = jugendherbergen

    self.update_rooms()

    if ("username" in properties):
      self.button_login_register.text = properties["username"]
      self.button_login_register.enabled = False

  def update_rooms(self):
    zimmerDaten = anvil.server.call("get_zimmerDaten")
    new_repeating_panel_1_items = []
    
    for v in zimmerDaten:
      selectedBerge = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
      if v[1] != selectedBerge:
        continue
      toAdd = {'id': v[0]}
      new_repeating_panel_1_items.append(toAdd)

    self.repeating_panel_1.items = new_repeating_panel_1_items
  
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.update_rooms()

  def button_login_register_click(self, **event_args):
    open_form('LoginRegister')
    pass
