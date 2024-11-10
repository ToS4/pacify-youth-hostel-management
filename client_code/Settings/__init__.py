from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    print(self.image_preview_profile_picture.source)
    self.init_components(**properties)
    self.check_login()
    username = anvil.server.call('get_username')
    if username:
      self.label_welcomer.text = f"Welcome, {username}"
    """profile_picture = anvil.server.call('get_profile_picture')
    if profile_picture:
      self.image_profilepicture.source = profile_picture
    else:
      self.image_profilepicture.source = self.get_default_profile_picture()"""
    

  def check_login(self):
    userId = anvil.server.call('get_user_id')
    #print(userId)
    if userId is None:
      self.button_login_logout.text = "Login / Register"
      #self.image_profilepicture.source = self.get_default_profile_picture()
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
    userId = anvil.server.call('get_user_id')
    if userId:
      anvil.server.call('logout')
    open_form('Home')

  def link_settings_click(self, **event_args):
    open_form('Settings')
    pass

  def file_loader_profile_picture_change(self, file, **event_args):
    print("file_loader_profile_picture_change", file)
    
    if file:
      self.image_preview_profile_picture.source = file
      self.image_profilepicture.source = file

  def handle_response(self, success, msg):
    self.label_responseMsg.text = ""
    self.label_responseMsg.foreground = "red"
    if success:
      self.label_responseMsg.foreground = "green"
    self.label_responseMsg.text = msg
  
  def button_save_click(self, **event_args):
    if self.image_profilepicture.source:
      anvil.server.call('save_profile_picture', self.image_profilepicture.source)

    if self.text_box_CurrentPassword.text != '':
      if self.text_box_NewPassword.text == '':
          self.handle_response(False, "Please enter a new password.")
      elif len(self.text_box_NewPassword.text) < 8:
          self.handle_response(False, "New password must be at least 8 characters long.")
      elif self.text_box_ConfirmPassword.text == '':
          self.handle_response(False, "Please confirm your new password.")
      elif self.text_box_ConfirmPassword.text != self.text_box_NewPassword.text:
          self.handle_response(False, "New password and confirm password do not match.")
      else:
          result, msg = anvil.server.call(
              'change_password', 
              current=self.text_box_CurrentPassword.text, 
              new=self.text_box_NewPassword.text
          )
          self.handle_response(result, msg)

        
      

