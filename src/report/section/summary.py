from datetime import datetime, timedelta

from base.type import ConfigType, CrawledDataType


class SummaryGenerator():
    def _formatted_summary(self, config: ConfigType) -> str:
        raise NotImplementedError()

    def generate_summary(self, data: CrawledDataType) -> str:
        iter_data = list(data.items())

        config = {
            "today_date": iter_data[-1][0],
            "today_cnt": iter_data[-1][1],
            "max_date": iter_data[-1][0],
            "max_cnt": iter_data[-1][1],
            "total_cnt": 0,
            "total_length": len(iter_data),
            "avg_cnt": 0,
            "cur_continous_start_date": iter_data[-1][0],
            "cur_continous_length": -1,
            "max_continous_start_date": iter_data[-1][0],
            "max_continous_length": 0,
            "max_continous_end_date": iter_data[-1][0],
        }

        tmp_continous_length = 0

        for date, cnt in reversed(iter_data):
            config["total_cnt"] += cnt
            if cnt > config["max_cnt"]:
                config["max_cnt"] = cnt
                config["max_date"] = date

            if cnt > 0:
                tmp_continous_length += 1
            else:
                # First zero means current continous length
                if config["cur_continous_length"] < 0:
                    config["cur_continous_length"] = config["max_continous_length"]
                    config["cur_continous_start_date"] = date

                tmp_continous_length = 0

            # Renew continous length
            if tmp_continous_length > config["max_continous_length"]:
                config["max_continous_length"] = tmp_continous_length
                config["max_continous_start_date"] = date

        if config["cur_continous_length"] < 0:
            config["cur_continous_length"] = config["max_continous_length"]
            config["cur_continous_start_date"] = date

        config["avg_cnt"] = config["total_cnt"] / config["total_length"]
        config["max_continous_end_date"] = config["max_continous_start_date"] + \
            timedelta(days=max(config["max_continous_length"]-1, 0))

        for key, value in config.items():
            if isinstance(value, datetime):
                config[key] = value.strftime("%Y-%m-%d")

        return self._formatted_summary(config=config)
