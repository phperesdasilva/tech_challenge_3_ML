from project.data_manager import DataManager
from project.model_builder import ModelBuilder


flights = 'database/flights.csv'
wanted_cols = wanted_cols = [
    'MONTH',
    'DAY_OF_WEEK',
    'AIRLINE',
    'ORIGIN_AIRPORT',
    'DESTINATION_AIRPORT',
    'SCHEDULED_DEPARTURE',
    'DISTANCE',
    'SCHEDULED_ARRIVAL',
    'DELAYED'
]

manager = DataManager()

df = manager.create_flights_dataframe(delay_limit=15, csv_path=flights)
filtered_df = manager.create_df_sample(df=df, percentage=1.5, wanted_cols=wanted_cols)
manager.show_stats(filtered_df)