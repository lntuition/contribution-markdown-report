from datetime import date
from typing import Sequence


class DateRange:
    def __init__(self, start: date, end: date) -> None:
        if end < start:
            raise Exception(f"{start} : Must be eariler than {end}")

        self.__start = start
        self.__end = end

    def __contains__(self, other: date) -> bool:
        return self.__start <= other <= self.__end

    # Current only iterate year for HTTP request
    def iter_year(self) -> Sequence[int]:
        return range(self.__start.year, self.__end.year + 1)
