import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas import DataFrame

class DataManager():

    def create_flights_dataframe(self, delay_limit: int, csv_path: str) -> DataFrame:
        df = pd.read_csv(csv_path, low_memory=False)
        df['DELAYED'] = np.where(df['ARRIVAL_DELAY'] >= delay_limit,1,0)
        return df
    
    def show_stats(self, df: DataFrame) -> None:
        columns = df.columns.tolist()
        print('\n\n')
        for i in range(len(columns)):
            print('col: ', columns[i], ' nunique: ', df[columns[i]].nunique(), '    total data: ', df[columns[i]].count(), '  nans: ', df[columns[i]].isna().sum())
        print('\n\n')

    def create_df_sample(self, df: DataFrame, percentage: int, wanted_cols: list[str]) -> DataFrame:
        filtered_df = df[wanted_cols]
        frac = percentage/100
        df_sample = filtered_df.sample(frac=frac, random_state=42)
        self.show_stats(df)
        return df_sample
    
    def compare(self, df: DataFrame, x: str, y: str) -> None:
        plot_df = df[[x, y]].dropna()
        plt.scatter(plot_df[x], plot_df[y], color='skyblue', alpha=0.6)
        plt.title(f'{y} x {x}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.grid(linestyle='--', alpha=0.7)
        plt.show()

    def hour_to_sec(self, df: DataFrame, col: str) -> None:
        data = df[col]
        hours = data // 100
        mins = data % 100
        df[col] = (hours * 3600) + (mins * 60)

    def min_to_sec(self, df: DataFrame, col: str):
        df[col] = df[col]*60