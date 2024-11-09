from ._anvil_designer import StatisticsTemplate
from anvil import *
import anvil.server

class Statistics(StatisticsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.check_login()
      
        bookings = anvil.server.call('get_bookings_by_user')
        print("statistics", bookings)

        self.data_grid_bookings.items = self.prepare_data_for_grid(bookings)    

    def check_login(self):
      userId = anvil.server.call('get_user_id')
      print(userId)
      if userId is None:
        self.button_login_logout.text = "Login / Register"
        open_form('LoginRegister')
      else:
        self.button_login_logout.text = "Logout"

    def prepare_data_for_grid(self, bookings):
        prepared_data = []
        for booking in bookings:
            prepared_data.append({
                'roomNr': booking[0],               
                'countBeds': booking[1],          
                'priceCategory': booking[2],          
                'location': booking[3],                
                'startdate': booking[4],             
                'enddate': booking[5],                
                'price': booking[6]                   
            })
        print(f"Prepared data for grid: {prepared_data}") # für debug
        return prepared_data

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
