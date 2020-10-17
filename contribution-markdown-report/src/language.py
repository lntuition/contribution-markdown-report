import warnings
from typing import Sequence


class LanguageSetting:  # pragma: no cover
    @staticmethod
    def header_title(user: str) -> str:
        return f"Welcome to {user}'s contribution report"

    @staticmethod
    def repository(url: str) -> str:
        return f"This report is generated by [contribution-markdown-report]({url})."

    @staticmethod
    def issue(url: str) -> str:
        return f"If you have any question or problem, please report [here]({url})."

    @staticmethod
    def ending() -> str:
        return "I hope this report will be a companion for your contribution trip."

    @staticmethod
    def summary_title() -> str:
        return "Summary"

    @staticmethod
    def today(date: str, count: str, length: str) -> str:
        return f"{date} was {length}th day since the start of trip, and there was {count} new contribution."

    @staticmethod
    def maximum(date: str, count: str) -> str:
        return f"Maximum contribution day is {date}, which is {count}."

    @staticmethod
    def total(_sum: str, avg: str) -> str:
        return f"During the trip, total contribuition count is {_sum} and average contribution count is {avg}."

    @staticmethod
    def today_peak(start_date: str, length: str) -> str:
        return f"Current continuous contribution trip is {length} days from {start_date}."

    @staticmethod
    def maximum_peak(start_date: str, end_date: str, length: str) -> str:
        return f"Longest continuous contribution trip was {length} days from {start_date} to {end_date}."

    @staticmethod
    def graph_title() -> str:
        return "Graph"

    @staticmethod
    def dayofweek_label() -> Sequence[str]:
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    @staticmethod
    def month_label() -> Sequence[str]:
        return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    @staticmethod
    def contribution_axis() -> str:
        return "contribution count"

    @staticmethod
    def day_axis() -> str:
        return "day"

    @staticmethod
    def dayofweek_axis() -> str:
        return "day of week"

    @staticmethod
    def month_axis() -> str:
        return "month"

    @staticmethod
    def year_axis() -> str:
        return "year"

    @staticmethod
    def count_sum_recent_title() -> str:
        return "Number of days per contribution up to the last 4 weeks"

    @staticmethod
    def count_sum_full_title() -> str:
        return "Number of days per contribution"

    @staticmethod
    def dayofweek_sum_recent_title() -> str:
        return "Number of contribution per day of week up to the last 12 weeks"

    @staticmethod
    def dayofweek_mean_full_title() -> str:
        return "Average of contribution per day of week"

    @staticmethod
    def month_sum_recent_title() -> str:
        return "Number of contribution per month up to the last year"

    @staticmethod
    def year_sum_full_title() -> str:
        return "Number of contribution per year"


class LanguageSettingFactory:
    @staticmethod
    def create_setting(language: str) -> LanguageSetting:
        default_language = "english"
        supported_language = {
            default_language: LanguageSetting,
        }

        if language.lower() not in supported_language:
            warnings.warn("Not supported languge, use default setting")
            language = default_language

        return supported_language[language]()