import pandas as pd


class Extractor:
    def __init__(self, user: str, df: pd.DataFrame) -> None:
        self.__user = user
        self.__df = df
