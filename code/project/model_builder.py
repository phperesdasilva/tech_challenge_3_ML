from pandas import DataFrame

class ModelBuilder():

    def __init__(self, df: DataFrame):
        self._df = df