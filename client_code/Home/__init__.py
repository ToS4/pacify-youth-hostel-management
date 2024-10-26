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

    #self.check_login()

  """  
  def check_login(self):
    user_id = anvil.server.session.get('user_id')
    if user_id is None:
      anvil.open_form('LoginRegister')"""
  
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
