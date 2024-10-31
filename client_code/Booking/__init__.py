from ._anvil_designer import BookingTemplate
from anvil import *
import anvil.tables as tables
from anvil.tables import app_tables
import datetime

class Booking(BookingTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.roomNr = properties["roomNr"]
        self.beds = properties["beds"]
        self.priceCategory = properties["priceCategory"]

        self.label_beds.text = f"{self.beds} beds" if self.beds else "N/A"
        self.label_location.text = f"Room {self.roomNr}" if self.roomNr else "N/A"
        self.label_priceCategory.text = self.priceCategory if self.priceCategory else "N/A"

        today = datetime.date.today()
        self.date_picker_startdate.date = today
        self.date_picker_startdate.min_date = today 

        self.date_picker_enddate.date = None
        self.date_picker_enddate.min_date = today + datetime.timedelta(days=1)
        
        self.price_per_night = self.get_price_per_night()
        self.total_price = self.price_per_night
        self.label_price.text = f"Total Price: ${self.total_price}"

    def get_price_per_night(self):
        if self.priceCategory == "Standard":
            base_price = 80
        elif self.priceCategory == "Premium":
            base_price = 150
        elif self.priceCategory == "Luxus":
            base_price = 300
        else:
            raise ValueError("Unbekannte Preiskategorie")
        
        price = base_price + (self.beds * 10)
        return price

    def update_price(self):
        print(f"Start date: {self.date_picker_startdate.date}, End date: {self.date_picker_enddate.date}")  # Debugging-Ausgabe
        if self.date_picker_startdate.date and self.date_picker_enddate.date:
            delta = (self.date_picker_enddate.date - self.date_picker_startdate.date).days
            print(f"Delta: {delta}") 
            if delta > 0:
                self.total_price = self.price_per_night * delta
            else:
                self.total_price = self.price_per_night
        else:
            self.total_price = self.price_per_night

        self.label_price.text = f"Total Price: ${self.total_price}"

    def date_picker_startdate_change(self, **event_args):
        print("Start date changed")  
        self.update_price()
     
        self.date_picker_enddate.min_date = self.date_picker_startdate.date + datetime.timedelta(days=1)

    def date_picker_enddate_change(self, **event_args):
        print("End date changed") 
        if self.date_picker_enddate.date <= self.date_picker_startdate.date:
            self.date_picker_enddate.date = self.date_picker_startdate.date + datetime.timedelta(days=1)
            print("End date adjusted to be one day after start date")  
        self.update_price()

    def button_book_booking_click(self, **event_args):
        if self.date_picker_startdate.date and self.date_picker_enddate.date and self.total_price > 0:
            app_tables.bookings.add_row(
                room_nr=self.roomNr,
                start_date=self.date_picker_startdate.date,
                end_date=self.date_picker_enddate.date,
                price=self.total_price
            )
            open_form('Statistics')
        else:
            alert("Bitte wählen Sie gültige Daten und versuchen Sie es erneut.")

    def link_home_click(self, **event_args):
        open_form('Home')

    def link_book_click(self, **event_args):
        open_form('Book')

    def link_statistics_click(self, **event_args):
        open_form('Statistics')
