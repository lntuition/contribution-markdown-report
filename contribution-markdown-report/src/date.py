from datetime import datetime, timedelta
from typing import Iterable


class DateFormatException(Exception):
    pass


class Date:
    def __init__(self, date: str) -> None:
        if date == "yesterday":  # Reserved keyword
            dt = datetime.now() - timedelta(days=1)
        else:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
            except ValueError as e:
                raise DateFormatException(f"{date} : wrong format") from e

        self.__year = dt.year
        self.__month = dt.month
        self.__day = dt.day

    @property
    def year(self) -> int:
        return self.__year

    def __lt__(self, other) -> bool:
        return int(self) < int(other)

    def __le__(self, other) -> bool:
        return int(self) <= int(other)

    def __ge__(self, other) -> bool:
        return int(self) >= int(other)

    def __gt__(self, other) -> bool:
        return int(self) > int(other)

    def __int__(self) -> int:
        return (self.__year * 10000) + (self.__month * 100) + self.__day

    def __repr__(self) -> str:
        return f"{self.__year}-{self.__month:02d}-{self.__day:02d}"


class DateIntervalException(Exception):
    pass


class DateInterval:
    def __init__(self, start: Date, end: Date) -> None:
        if end < start:
            raise DateIntervalException(f"{start} : eariler than {end}")

        self.__start = start
        self.__end = end

    def __contains__(self, date: Date) -> bool:
        return self.__start <= date <= self.__end

    def iter_year(self) -> Iterable[int]:
        return range(self.__start.year, self.__end.year + 1)
