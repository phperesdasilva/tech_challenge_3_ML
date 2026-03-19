import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DataManager():

    def create_flights_dataframe(self, delay_limit: int, csv_path: str) -> DataFrame:
        df = pd.read_csv(csv_path, low_memory=False)
        df['DELAYED'] = np.where(df['ARRIVAL_DELAY'] >= delay_limit,1,0)
        df = df[df['CANCELLED'] == 0]
        df = df[df['DIVERTED'] == 0]
        return df
    
    def create_aux_features(self, filtered_df: DataFrame) -> DataFrame:

        bins = [0, 43200, 64800, 86400] #transformed to seconds
        labels = ['MORNING', 'AFTERNOON', 'EVENING']
        filtered_df['PERIOD'] = pd.cut(
            filtered_df['SCHEDULED_DEPARTURE'], 
            bins=bins, 
            labels=labels, 
            right=False, # ensure 12h (43200) will be AFTERNOON
            include_lowest=True
        ).astype(str)

        # North Hemisphere
        # Winter: Dez(12), Jan(1), Feb(2)
        # Spring: Mar(3), Apr(4), May(5)
        # Summer: Jun(6), Jul(7), Ago(8)
        # Fall: Set(9), Out(10), Nov(11)

        season_map = {
            12: 'WINTER', 1: 'WINTER', 2: 'WINTER',
            3: 'SPRING', 4: 'SPRING', 5: 'SPRING',
            6: 'SUMMER', 7: 'SUMMER', 8: 'SUMMER',
            9: 'FALL', 10: 'FALL', 11: 'FALL'
        }

        filtered_df['SEASON'] = filtered_df['MONTH'].map(season_map)

        # EUA holidays:
        # 1: New Year / MLK Day
        # 5: Memorial Day
        # 7: Independence Day
        # 11: Thanksgiving
        # 12: Christmas

        #comparar quantidade de 1 e 0 na base de dados filtrada
        #pode ser que isso não seja necessario, testar sem isso
        holiday_months = [1, 5, 7, 11, 12]
        filtered_df['HOLIDAY'] = filtered_df['MONTH'].isin(holiday_months).astype(int)
        
        return filtered_df

    def show_stats(self, df: DataFrame) -> None:
        columns = df.columns.tolist()
        print('\n\n')
        #print('total data:\n',df.count())
        print('\n')
        for i in range(len(columns)):
            print('col: ', (30-len(columns[i]))*'-',
                columns[i],
                '  nans: ',
                df[columns[i]].isna().sum(),
                ' unique values: ',
                df[columns[i]].nunique())
        print('\n\n')

    def create_df_sample(self, df: DataFrame, percentage: float, wanted_cols: list[str]) -> DataFrame:
        filtered_df = df[wanted_cols]
        frac = percentage/100
        df_sample = filtered_df.sample(frac=frac, random_state=42)
        df_sample = df_sample.dropna()
        return df_sample
    
    def compare(self, df: DataFrame, x: str, y: str) -> None:
        plot_df = df[[x, y]].dropna()
        plt.scatter(plot_df[x], plot_df[y], color='skyblue', alpha=0.6)
        plt.title(f'{y} x {x}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.grid(linestyle='--', alpha=0.7)
        plt.show()

    def hour_to_sec(self, df: DataFrame, cols: list[str]) -> None:
        for col in cols:
            data = df[col]
            hours = data // 100
            mins = data % 100
            df[col] = (hours * 3600) + (mins * 60)

    def min_to_sec(self, df: DataFrame, cols: list[str]):
        for col in cols:
            df[col] = df[col]*60

    def encode_df(self, df: DataFrame)  -> DataFrame:
        le = LabelEncoder()

        df = pd.get_dummies(df, columns=['SEASON', 'PERIOD'])
        df['AIRLINE_COD'] = le.fit_transform(df['AIRLINE'])
        df['ORIGIN_AIRPORT_COD'] = le.fit_transform(df['ORIGIN_AIRPORT'])
        df['DESTINATION_AIRPORT_COD'] = le.fit_transform(df['DESTINATION_AIRPORT'])
        df['FLIGHT_NUMBER_COD'] = le.fit_transform(df['FLIGHT_NUMBER'])
        
        cols_to_remove = ['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'FLIGHT_NUMBER']
        df = df.drop(columns=cols_to_remove)
        return df
    
    def get_test_split(self, df: DataFrame, target: str) -> list[DataFrame]:
          
        features = df.columns.tolist()
        features.remove(target)
          
        x = df[features]
        y = df[target]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)
        
        # cat_df = df.select_dtypes(include=['string'])
        # cat_cols = cat_df.columns.tolist()
        
        #testar one-hot encoding para estação do ano
        #testar label encoding
        #com certeza usar label encoding em airline, origin_airport, destination_airport
        #talvez procurar as companias mais significativas e agrupar por 
        
        # encoder = TargetEncoder(cols=cat_cols, smoothing=20.0)
        # x_train_encoded = encoder.fit_transform(x_train, y_train)
        # x_test_encoded = encoder.transform(x_test)
        return [x_train, x_test, y_train, y_test]