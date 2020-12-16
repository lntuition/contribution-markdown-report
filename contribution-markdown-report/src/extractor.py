import pandas as pd


class Extractor:
    def __init__(self, user: str, df: pd.DataFrame):
        self.__user = user
        self.__df = df

    @property
    def user(self) -> str:
        return self.__user

    @property
    def df(self) -> pd.DataFrame:
        return self.__df
