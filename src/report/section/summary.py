import pandas as pd

from datetime import datetime

from base.type import ConfigType


class SummaryGenerator():
    def _formatted_summary(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def _continous_config(self, data: pd.DataFrame) -> ConfigType:
        config = {}

        active = pd.Series(data=(data["count"] > 0))
        continous = active * (active.groupby(
            (active != active.shift()).cumsum()
        ).cumcount() + 1)

        total_length = len(data.index)
        cur_continous_length = continous.iloc[-1]

        config["cur_continous_length"] = cur_continous_length
        config["cur_continous_start_date"] = data.loc[
            total_length - 1 - max(0, cur_continous_length-1)
        ]["date"]

        max_continous_idx = continous.idxmax()
        max_continous_length = continous.loc[max_continous_idx]

        config["max_continous_length"] = max_continous_length
        config["max_continous_end_date"] = data.loc[max_continous_idx]["date"]
        config["max_continous_start_date"] = data.loc[
            max_continous_idx - max(0, max_continous_length-1)
        ]["date"]

        return config

    def _brief_config(self, data: pd.DataFrame) -> ConfigType:
        config = {}

        config["total_length"] = len(data.index)

        counts = data["count"]
        config["total_cnt"] = counts.sum()
        config["avg_cnt"] = counts.mean()

        today = data.iloc[-1]
        config["today_date"] = today["date"]
        config["today_cnt"] = today["count"]

        maximum = data.iloc[counts.idxmax()]
        config["max_date"] = maximum["date"]
        config["max_cnt"] = maximum["count"]

        return config

    def generate_summary(self, data: pd.DataFrame) -> str:
        config = {
            **self._brief_config(data=data),
            **self._continous_config(data=data)
        }

        for key, value in config.items():
            if isinstance(value, datetime):
                config[key] = value.strftime("%Y-%m-%d")

        return self._formatted_summary(config=config)
