import pandas as pd

class Pickle:

    def __init__(self):
        pass

    def save(self, df, name):
        df.to_pickle(f"data_managing/files/{name}.pkl")

    def load(self, name):
        return pd.read_pickle(f"data_managing/files/{name}.pkl")