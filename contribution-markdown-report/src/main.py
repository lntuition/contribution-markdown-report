from crawler import Crawler
from date import Date, DateInterval
from report import Report
from repository import Repository, RepositoryURL
from section.graph import GraphSection, GraphSettingFactory
from section.header import HeaderSection, HeaderSettingFactory
from section.summary import SummarySection, SummarySettingFactory
from util import safe_chdir, safe_environ

if __name__ == "__main__":
    user = safe_environ("GITHUB_ACTOR")
    end = Date(date="yesterday")
    language = safe_environ("INPUT_LANGUAGE")

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
    work_path = safe_environ("INPUT_PATH")

    header_setting = HeaderSettingFactory.create_setting(language=language)
    header_section = HeaderSection(user=user, setting=header_setting)

    summary_setting = SummarySettingFactory.create_setting(language=language)
    summary_section = SummarySection(data=data, setting=summary_setting)

    graph_setting = GraphSettingFactory.create_setting(language=language)
    graph_section = GraphSection(data=data, setting=graph_setting)

    sections = [header_section, summary_section, graph_section]
    with safe_chdir(repo.workdir):
        Report.generate(sections=sections, path=work_path)

    repo.add(path=work_path)
    repo.commit(
        msg=f"BOT : {end} contribution report",
        email=safe_environ("INPUT_AUTHOR_EMAIL"),
        name=safe_environ("INPUT_AUTHOR_NAME"),
    )
    repo.push()
