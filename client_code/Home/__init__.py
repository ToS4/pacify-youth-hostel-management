from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.check_login()

  def check_login(self):
    userId = anvil.server.call('get_user_id')
    #print(userId)
    if userId is None:
      self.button_login_logout.text = "Login / Register"
    else:
      self.button_login_logout.text = "Logout"
  
  def link_home_click(self, **event_args):
    open_form('Home')

  def link_book_click(self, **event_args):
    open_form('Book')

  def link_statistics_click(self, **event_args):
    open_form('Statistics')

  def button_login_logout_click(self, **event_args):
    userId = anvil.server.call('get_user_id')
    if userId is None:
      open_form('LoginRegister')
    else:
      anvil.server.call('logout')
      self.button_login_logout.text = "Login / Register"

