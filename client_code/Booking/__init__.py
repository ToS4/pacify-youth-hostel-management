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
    roomNr = properties["roomNr"]
    beds = properties["beds"]
    priceCategory = properties["priceCategory"]

    print(roomNr, beds, priceCategory)
    
  def button_book_booking_click(self, **event_args):
    open_form('Statistics')

  def link_home_click(self, **event_args):
    open_form('Home')

  def link_book_click(self, **event_args):
    open_form('Book')

  def link_statistics_click(self, **event_args):
    open_form('Statistics')

  
