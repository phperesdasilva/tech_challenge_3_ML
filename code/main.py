from project.data_manager import DataManager
from project.model_builder import ModelBuilder


flights = 'database/flights.csv'
wanted_cols = [
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
filtered_df = manager.create_df_sample(df=df, percentage=2, wanted_cols=wanted_cols)

hours_to_transform = [
    'SCHEDULED_DEPARTURE',
    'SCHEDULED_ARRIVAL'
]

manager.hour_to_sec(df=filtered_df, cols=hours_to_transform)

filtered_df = manager.create_aux_features(filtered_df=filtered_df)

filtered_df = filtered_df.drop('HOLIDAY', axis=1)

[x_train, x_test, y_train, y_test] = manager.get_test_split(df=filtered_df, target='DELAYED')
