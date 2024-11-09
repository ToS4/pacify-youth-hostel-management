from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.check_login()
    username = anvil.server.call('get_username')
    if username:
      self.label_welcomer.text = f"Welcome, {username}"

  def check_login(self):
    userId = anvil.server.call('get_user_id')
    #print(userId)
    if userId is None:
      self.button_login_logout.text = "Login / Register"
      open_form('LoginRegister')
    else:
      self.button_login_logout.text = "Logout"

  def link_home_click(self, **event_args):
    open_form("Home")

  def link_book_click(self, **event_args):
    open_form("Book")

  def link_statistics_click(self, **event_args):
    open_form("Statistics")

  def button_login_logout_click(self, **event_args):
    userId = anvil.server.call("get_user_id")
    if userId is None:
      open_form("LoginRegister")
    else:
      anvil.server.call("logout")
      self.button_login_logout.text = "Login / Register"

  def link_settings_click(self, **event_args):
    open_form('Settings')
    pass

  def file_loader_profile_picture_change(self, file, **event_args):
    print("file_loader_profile_picture_change", file)
    self.image_preview_profile_picture.source = file

  def button_save_click(self, **event_args):
    pass
