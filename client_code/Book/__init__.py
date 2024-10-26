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
  
  def button_login_register_click(self, **event_args):
    open_form('LoginRegister')
    pass

  
  
  

 