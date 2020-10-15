from datetime import datetime, timedelta
from typing import Sequence


class Date:
    def __init__(self, date: str) -> None:
        if date == "yesterday":  # Reserved keyword
            std_date = datetime.now() - timedelta(days=1)
        else:
            try:
                std_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError as error:
                raise Exception(f"{date} : Wrong date format") from error

        self.__year = std_date.year
        self.__month = std_date.month
        self.__day = std_date.day

    @property
    def year(self) -> int:
        return self.__year

    def __lt__(self, other) -> bool:
        return str(self) < str(other)

    def __le__(self, other) -> bool:
        return str(self) <= str(other)

    def __ge__(self, other) -> bool:
        return str(self) >= str(other)

    def __gt__(self, other) -> bool:
        return str(self) > str(other)

    def __repr__(self) -> str:
        return f"{self.__year}-{self.__month:02d}-{self.__day:02d}"


class DateInterval:
    def __init__(self, start: Date, end: Date) -> None:
        if end < start:
            raise Exception(f"{start} : Must be eariler than {end}")

        self.__start = start
        self.__end = end

    def __contains__(self, date: Date) -> bool:
        return self.__start <= date <= self.__end

    def iter_year(self) -> Sequence[int]:
        return range(self.__start.year, self.__end.year + 1)
