from abc import ABCMeta, abstractmethod
from typing import List


class HeaderSetting(metaclass=ABCMeta):
    @abstractmethod
    def header_greeting(self, username: str) -> str:
        pass

    @abstractmethod
    def header_notice(self, repo_url: str, issue_url: str) -> str:
        pass


class SummarySetting(metaclass=ABCMeta):
    @abstractmethod
    def summary_title(self) -> str:
        pass

    @abstractmethod
    def summary_today(self, today: str, length: str, count: str) -> str:
        pass

    @abstractmethod
    def summary_maximum(self, date: str, count: str) -> str:
        pass

    @abstractmethod
    def summary_total(self, sum: str, avg: str) -> str:
        pass

    @abstractmethod
    def summary_peak(self, length: str, start: str, end: str) -> str:
        pass

    @abstractmethod
    def summary_cur_peak(self, length: str, start: str) -> str:
        pass


class GraphSetting(metaclass=ABCMeta):
    @abstractmethod
    def graph_title(self) -> str:
        pass

    @abstractmethod
    def graph_dayofweek_label(self) -> List[str]:
        pass

    def graph_month_label(self) -> List[str]:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    @abstractmethod
    def graph_contribution_axis(self) -> str:
        pass

    @abstractmethod
    def graph_day_axis(self) -> str:
        pass

    @abstractmethod
    def graph_dayofweek_axis(self) -> str:
        pass

    @abstractmethod
    def graph_month_axis(self) -> str:
        pass

    @abstractmethod
    def graph_count_sum_recent_title(self) -> str:
        pass

    @abstractmethod
    def graph_count_sum_full_title(self) -> str:
        pass

    @abstractmethod
    def graph_dayofweek_sum_recent_title(self) -> str:
        pass

    @abstractmethod
    def graph_dayofweek_mean_full_title(self) -> str:
        pass

    @abstractmethod
    def graph_month_sum_recent_title(self) -> str:
        pass

    @abstractmethod
    def graph_month_mean_full_title(self) -> str:
        pass


class LanguageSetting(HeaderSetting, SummarySetting, GraphSetting, metaclass=ABCMeta):
    pass
