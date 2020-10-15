from .report import Report
from .repository import Repository


class Work:
    @staticmethod
    def with_repository(repository: Repository, report: Report) -> None:
        repository.generate(report=report)
        repository.add()
        repository.commit(report=report)
        repository.push()

    @staticmethod
    def without_repository(report: Report) -> None:
        report.generate()
