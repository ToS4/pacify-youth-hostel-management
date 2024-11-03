from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.button_book_home.foreground = "white"
    self.button_book_home.background = "purple"

  def button_book_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form(
        'Booking',
        RID=self.item['roomNr'],            
        beds=self.item['countBeds'],
        priceCategory=self.item['priceCategory']
    )
    
    
    pass
