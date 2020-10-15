from unittest.mock import MagicMock, call

import pytest

from src.work import Work


class TestWork:
    def test_with_repository(self) -> None:
        mock_repository = MagicMock()
        mock_report = MagicMock()

        Work.with_repository(repository=mock_repository, report=mock_report)

        mock_repository.assert_has_calls(
            [
                call.generate(report=mock_report),
                call.add(),
                call.commit(report=mock_report),
                call.push(),
            ]
        )

    def test_without_repository(self) -> None:
        mock_report = MagicMock()

        Work.without_repository(report=mock_report)

        mock_report.assert_has_calls(
            [
                call.generate(),
            ]
        )
