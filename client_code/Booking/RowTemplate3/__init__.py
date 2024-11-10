from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_remove_click(self, **event_args):
    """This method is called when the button is clicked"""
    drop_down_addUser_items = get_open_form().drop_down_addUser.items
    repeating_panel_added_users_items = get_open_form().repeating_panel_added_users.items

    new_drop_down_addUser_items = []
    new_repeating_panel_added_users_items = []

    user_to_remove = self.item['addedUser']
    
    for item in drop_down_addUser_items:
      #print("drop_down_addUser_items", item)
      new_drop_down_addUser_items.append(item)

    for item in repeating_panel_added_users_items:
      #print("repeating_panel_added_users_items", item)

      if item["addedUser"] == user_to_remove:
        new_drop_down_addUser_items.append((user_to_remove, user_to_remove))
        continue
      
      new_repeating_panel_added_users_items.append(item)

    get_open_form().drop_down_addUser.items = new_drop_down_addUser_items
    get_open_form().repeating_panel_added_users.items = new_repeating_panel_added_users_items

    
  
