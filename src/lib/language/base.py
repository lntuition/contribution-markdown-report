from abc import ABCMeta, abstractmethod


class HeaderSetting(metaclass=ABCMeta):
    @abstractmethod
    def header_greeting(self, username: str) -> str:
        pass

    @abstractmethod
    def header_notice(self, repo_url: str, issue_url: str) -> str:
        pass


class SummarySetting(metaclass=ABCMeta):
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
    def config_graph(self):
        pass


class LanguageSetting(HeaderSetting, SummarySetting, GraphSetting, metaclass=ABCMeta):
    pass
