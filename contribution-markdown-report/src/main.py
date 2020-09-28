import os
import sys
import traceback
from functools import reduce

from crawler import crawl_data
from date import Date, DateInterval
from language.factory import language_setting_factory
from repository import Repository, RepositoryURL
from section.graph import GraphGenerator
from section.header import HeaderGenerator
from section.summary import SummaryGenerator
from util import safe_chdir, safe_environ

if __name__ == "__main__":
    try:
        user = safe_environ("GITHUB_ACTOR")
        end = Date(date="yesterday")

        repo_url = RepositoryURL(
            user=user,
            token=safe_environ("INPUT_GITHUB_TOKEN"),
            name=safe_environ("GITHUB_REPOSITORY"),
        )
        repo = Repository(url=repo_url, path=safe_environ("OUTPUT_PATH"), branch=safe_environ("INPUT_BRANCH"))

        data = crawl_data(user=user, interval=DateInterval(start=Date(date=safe_environ("INPUT_START_DATE")), end=end))
        setting = language_setting_factory(language=safe_environ("INPUT_LANGUAGE"))

        generate_path = os.path.join(repo.workdir, safe_environ("INPUT_PATH"))

        # Generate
        with safe_chdir(generate_path), open("README.md", "w") as fp:
            fp.write(
                reduce(
                    lambda a, b: a + b,
                    map(
                        lambda x: x.generate(),
                        [
                            HeaderGenerator(
                                username=user,
                                setting=setting,
                            ),
                            SummaryGenerator(
                                data=data,
                                setting=setting,
                            ),
                            GraphGenerator(
                                data=data,
                                setting=setting,
                            ),
                        ],
                    ),
                )
            )

        repo.add(path=generate_path)
        repo.commit(
            msg=f"BOT : {end} contribution report",
            email=safe_environ("INPUT_AUTHOR_EMAIL"),
            name=safe_environ("INPUT_AUTHOR_NAME"),
        )
        repo.push()

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
