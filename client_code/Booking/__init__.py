from ._anvil_designer import BookingTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Booking(BookingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_book_booking_click(self, **event_args):
    open_form('Statistik')
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

  
