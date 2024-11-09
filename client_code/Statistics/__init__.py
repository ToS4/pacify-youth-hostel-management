from ._anvil_designer import StatisticsTemplate
from anvil import *
import anvil.server

class Statistics(StatisticsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.check_login()
      
        bookings = anvil.server.call('get_bookings_by_user')
        #print("statistics", bookings)

        self.update_bookings(bookings)

    def check_login(self):
      userId = anvil.server.call('get_user_id')
      #print(userId)
      if userId is None:
        self.button_login_logout.text = "Login / Register"
        open_form('LoginRegister')
      else:
        self.button_login_logout.text = "Logout"

    def update_bookings(self, bookings):
      prepared_bookings = []
      for booking in bookings:
          toAdd = {
              'roomNr': booking[0],
              'startdate': booking[1],             
              'enddate': booking[2],                
              'countBeds': booking[3], 
              'priceCategory': booking[4],
              'location': booking[5],                
              'price': booking[6]   
          }
          prepared_bookings.append(toAdd)
      
      self.repeating_panel_statistics.items = prepared_bookings
      #print(prepared_bookings)
      
    def link_home_click(self, **event_args):
        open_form('Home')

    def link_book_click(self, **event_args):
        open_form('Book')

    def link_statistics_click(self, **event_args):
        open_form('Statistics')
  
    def button_login_register_click(self, **event_args):
      userId = anvil.server.call('get_user_id')
      if userId:
        anvil.server.call('logout')
      open_form('Home')

    def link_settings_click(self, **event_args):
      open_form('Settings')
        
