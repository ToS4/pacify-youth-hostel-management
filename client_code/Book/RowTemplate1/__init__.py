from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_book_home.foreground = "white"
    self.button_book_home.background = "purple"
    # Any code you write here will run before the form opens.

  
  def button_book_home_click(self, **event_args):
    selected_location = get_open_form().drop_down_location.selected_value
    #print(f"Selected Location: {selected_location}") 
    if isinstance(selected_location, list) and len(selected_location) > 2:
        city_name = selected_location[2]
    else:
        city_name = "Unbekannt"

    #print(f"City Name: {city_name}")

    open_form(
        'Booking',
        RID=self.item['RID'],
        roomNr=self.item['roomNr'],
        beds=self.item['countBeds'],
        priceCategory=self.item['priceCategory'], 
        location=city_name  
    )