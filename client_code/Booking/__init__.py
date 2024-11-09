from ._anvil_designer import BookingTemplate
from anvil import *
import anvil.tables as tables
from anvil.tables import app_tables
import datetime
import anvil.server

class Booking(BookingTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.roomNr = properties["roomNr"]
        self.beds = properties["beds"]
        self.location = properties.get("location", "Unknown") 
        self.priceCategory = properties["priceCategory"]

        self.label_beds.text = f"{self.beds} beds" if self.beds else "N/A"
        self.label_location.text = f"{self.location}" if self.location else "N/A"
        self.label_priceCategory.text = self.priceCategory if self.priceCategory else "N/A"

        today = datetime.date.today()
        self.date_picker_startdate.date = today
        self.date_picker_startdate.min_date = today 

        self.date_picker_enddate.date = None
        self.date_picker_enddate.min_date = today + datetime.timedelta(days=1)
        
        self.price_per_night = self.get_price_per_night()
        self.total_price = self.price_per_night
        self.label_price.text = f"Total Price: ${self.total_price}"

        self.update_user_dropdown() 
        self.check_login()

    def check_login(self):
      userId = anvil.server.call('get_user_id')
      print(userId)
      if userId is None:
        self.button_login_logout.text = "Login / Register"
        open_form('LoginRegister')
      else:
        self.button_login_logout.text = "Logout"

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
        print(f"Start date: {self.date_picker_startdate.date}, End date: {self.date_picker_enddate.date}")
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
            try:
                anvil.server.call(
                    'save_booking',
                    room_nr=self.roomNr,
                    start_date=self.date_picker_startdate.date,
                    end_date=self.date_picker_enddate.date,
                    price=self.total_price,
                )
                open_form('Statistics')
            except Exception as e:
                alert(f"Fehler beim Speichern der Buchung: {e}")
        else:
            alert("Bitte wählen Sie gültige Daten und versuchen Sie es erneut.")

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
                          
    def update_user_dropdown(self):
        try:
            usernames = anvil.server.call('get_all_users')
            print(f"Users retrieved: {usernames}")
            self.drop_down_addUser.items = usernames
            self.drop_down_addUser.selected_value = ""
        except Exception as e:
            alert(f"Fehler beim Abrufen der Benutzerdaten: {e}")

        
    def drop_down_addUser_change(self, **event_args):
        """This method is called when an item is selected"""
        selected_user = self.drop_down_addUser.selected_value

        if selected_user and selected_user != "":
            current_items = self.repeating_panel_added_users.items

            toAdd = {
                'addedUser': selected_user,        
            }
            
            current_items.append(toAdd)
            
            self.data_grid_Added_Users.items = current_items
            
            


    
    def data_grid_Added_Users_click(self, row, **event_args):
      if row.get('remove_users') == "Entfernen":
        current_items = self.data_grid_Added_Users.items
        current_items.remove(row)
        self.data_grid_Added_Users.items = current_items