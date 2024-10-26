from ._anvil_designer import LoginRegisterTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class LoginRegister(LoginRegisterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #styling
    self.button_login.background = "green"
    self.button_register.background = "green" 
    self.button_login.foreground = "white"
    self.button_register.foreground = "white" 
    # Any code you write here will run before the form opens.

  def button_register_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')
    pass

  def button_login_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')
    pass