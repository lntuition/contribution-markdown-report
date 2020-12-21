from __future__ import annotations

import warnings
from typing import Dict, Type


class MessageSkeleton:
    __skeleton = {
        "english": {
            "message": {
                "greeting": "Welcome to {user}'s contribution report",
                "source": "This report is generated by [contribution-markdown-report]({link}).",
                "inquiry": "If you have any question or problem, please report [here]({link}).",
                "summary": "Summary for contribution",
                "today": "{date} was {length}th day since the start of trip, and there was {count} new contribution.",
                "today-peak": "Current continuous contribution trip is {length} days from {start}.",
                "max": "Maximum contribution day is {date}, which is {count}.",
                "max-peak": "Longest continuous contribution trip was {length} days from {start} to {end}.",
                "total": "During the trip, total contribuition count is {sum} and average contribution count is {avg}.",
                "graph": "Graph for contribution",
            },
            "label": {
                "dayofweek": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            },
            "axis": {
                "contribution_count": "contribution count",
                "day": "day",
                "dayofweek": "dayofweek",
                "month": "month",
                "year": "year",
            },
            "graph": {
                "count-sum-recent": "Number of days per contribution up to the last 4 weeks",
                "count-sum-full": "Number of days per contribution",
                "dayofweek-sum-recent": "Number of contribution per day of week up to the last 12 weeks",
                "dayofweek-mean-full": "Average of contribution per day of week",
                "month-sum-recent": "Number of contribution per month up to the last year",
                "year-sum-full": "Number of contribution per year",
            },
        },
    }

    @classmethod
    def get_skeleton(
        cls: Type[MessageSkeleton],
        language: str,
    ) -> Dict[str, object]:
        # TODO : Fix type error with detail return type
        default_language = "english"
        supported_language = [
            default_language,  # english
        ]

        if language.lower() not in supported_language:
            warnings.warn("Not supported languge, use default setting")
            language = default_language

        return cls.__skeleton[language]
