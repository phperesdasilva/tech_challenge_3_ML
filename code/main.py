from project.data_manager import DataManager
from project.model_builder import ModelBuilder


flights = 'database/flights.csv'

manager = DataManager()

df = manager.create_flights_dataframe(delay_limit=15, csv_path=flights)
