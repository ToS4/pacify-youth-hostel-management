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
    self.button_login.foreground = "white"
    
    self.button_register.background = "green" 
    self.button_register.foreground = "white" 

    self.text_box_username.background = "white"
    self.text_box_password.background = "white"
  
    # Any code you write here will run before the form opens.

  def handle_response(self, success, msg):
    self.label_responseMsg.text = ""
    self.label_responseMsg.foreground = "red"
    if success:
      self.label_responseMsg.foreground = "green"
      open_form('Home')
    self.label_responseMsg.text = msg
    
  def button_register_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    username = self.text_box_username.text
    password = self.text_box_password.text

    success, msg = anvil.server.call('register', username, password)
    self.handle_response(success, msg)

  def button_login_click(self, **event_args):
    """This method is called when the button is clicked"""

    username = self.text_box_username.text
    password = self.text_box_password.text

    success, msg = anvil.server.call('login', username, password)
    self.handle_response(success, msg)

    