from ._anvil_designer import StatisticsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Book import Book
from ..Home import Home

class Statistics(StatisticsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_statistics_click(self, **event_args):
    pass

  def link_home_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    pass

  def link_book_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Book())
    pass
