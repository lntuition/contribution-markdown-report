from crawler import Crawler
from date import Date, DateInterval
from report import Report
from repository import Repository, RepositoryURL
from setting import SettingFactory
from util import safe_chdir, safe_environ
from writer import GraphWriter, HeaderWriter, SummaryWriter

if __name__ == "__main__":
    user = safe_environ("GITHUB_ACTOR")
    end = Date(date="yesterday")

    repo_url = RepositoryURL(
        user=user,
        token=safe_environ("INPUT_GITHUB_TOKEN"),
        name=safe_environ("GITHUB_REPOSITORY"),
    )
    repo = Repository(
        url=repo_url,
        path=safe_environ("OUTPUT_PATH"),
        branch=safe_environ("INPUT_BRANCH"),
    )

    data = Crawler.execute(
        user=user,
        interval=DateInterval(start=Date(date=safe_environ("INPUT_START_DATE")), end=end),
    )
    settings = SettingFactory.create_settings(language=safe_environ("INPUT_LANGUAGE"))

    work_path = safe_environ("INPUT_PATH")

    writers = [HeaderWriter(user=user), SummaryWriter(data=data), GraphWriter(data=data)]

    with safe_chdir(repo.workdir):
        Report.generate(writers=writers, settings=settings, path=work_path)

    repo.add(path=work_path)
    repo.commit(
        msg=f"BOT : {end} contribution report",
        email=safe_environ("INPUT_AUTHOR_EMAIL"),
        name=safe_environ("INPUT_AUTHOR_NAME"),
    )
    repo.push()
