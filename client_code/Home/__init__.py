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

    self.check_login()

  def check_login(self):
    userId = anvil.server.call('get_user_id')
    print(userId)
    if userId is None:
      pass
  
  def link_home_click(self, **event_args):
    open_form('Home')
    pass

  def link_book_click(self, **event_args):
    open_form('Book')
    pass

  def link_statistics_click(self, **event_args):
    open_form('Statistics')
    pass

  def button_login_logout_click(self, **event_args):
    open_form('LoginRegister')
    pass
