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

  
    profile_picture = anvil.server.call('get_profile_picture')
    if profile_picture:
        self.image_profilepicture.source = profile_picture

    
  def check_login(self):
    userId = anvil.server.call('get_user_id')
    #print(userId)
    if userId is None:
      self.button_login_logout.text = "Login / Register"
      #self.image_profilepicture.source = self.get_default_profile_picture()
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
      self.image_profilepicture.source = anvil.server.call('get_default_profile_picture')
      self.button_login_logout.text = "Login / Register"

  def link_settings_click(self, **event_args):
    open_form('Settings')

