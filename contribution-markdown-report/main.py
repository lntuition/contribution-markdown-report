import os

from src.contribution import ContributionInfoCollector
from src.date import Date
from src.language import LanguageSettingFactory
from src.report import Report
from src.repository import Repository, RepositoryActorBuilder, RepositoryCoreBuilder
from src.work import Work

if __name__ == "__main__":
    Work.with_repository(
        repository=Repository(
            core=RepositoryCoreBuilder.build(
                user=os.environ["GITHUB_ACTOR"],
                token=os.environ["INPUT_GITHUB_TOKEN"],
                repository=os.environ["GITHUB_REPOSITORY"],
                branch=os.environ["INPUT_BRANCH"],
            ),
            actor=RepositoryActorBuilder.build(
                name=os.environ["INPUT_AUTHOR_NAME"],
                email=os.environ["INPUT_AUTHOR_EMAIL"],
            ),
            work_dir=os.environ["INPUT_PATH"],
        ),
        report=Report(
            info=ContributionInfoCollector(
                user=os.environ["GITHUB_ACTOR"],
                start=Date(os.environ["INPUT_START_DATE"]),
                end=Date("yesterday"),
            ).collect(),
            setting=LanguageSettingFactory.create_setting(
                language=os.environ["INPUT_LANGUAGE"],
            ),
            headings=[
                "header",
                "summary",
                "graph",
            ],
            file_name="README.md",
        ),
    )
