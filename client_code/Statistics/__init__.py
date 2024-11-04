from ._anvil_designer import StatisticsTemplate
from anvil import *
import anvil.server

class Statistics(StatisticsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        userId = anvil.server.call('get_user_id')
        bookings = anvil.server.call('get_bookings_by_user', userId)
        print(bookings)

        self.data_grid_bookings.items = self.prepare_data_for_grid(bookings)

        self.check_login()

    def check_login(self):
      userId = anvil.server.call('get_user_id')
      print(userId)
      if userId is None:
        self.button_login_logout.text = "Login / Register"
      else:
        self.button_login_logout.text = "Logout"

    def prepare_data_for_grid(self, bookings):
        prepared_data = []
        for booking in bookings:
            prepared_data.append({
                'roomNr': booking[1],               
                'countBeds': booking[2],          
                'priceCategory': booking[3],          
                'location': booking[4],                
                'startdate': booking[5],             
                'enddate': booking[6],                
                'price': booking[7]                   
            })
        print(f"Prepared data for grid: {prepared_data}") # für debug
        return prepared_data

    def link_home_click(self, **event_args):
        open_form('Home')

    def link_book_click(self, **event_args):
        open_form('Book')

    def link_statistics_click(self, **event_args):
        open_form('Statistics')
