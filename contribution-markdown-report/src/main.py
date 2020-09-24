import os
import sys
import traceback
from datetime import datetime, timedelta
from functools import reduce

from crawler import crawl_data
from directory import change_workdir
from language.factory import language_setting_factory
from repository import Repository, RepositoryURL
from section.graph import GraphGenerator
from section.header import HeaderGenerator
from section.summary import SummaryGenerator
from util import safe_environ

if __name__ == "__main__":
    try:
        user = safe_environ("GITHUB_ACTOR")
        finish = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        repo_url = RepositoryURL(
            user=user,
            token=safe_environ("INPUT_GITHUB_TOKEN"),
            name=safe_environ("GITHUB_REPOSITORY"),
        )
        repo = Repository(url=repo_url, path=safe_environ("OUTPUT_PATH"), branch=safe_environ("INPUT_BRANCH"))

        data = crawl_data(
            username=user,
            start=safe_environ("INPUT_START_DATE"),
            finish=finish,
        )
        setting = language_setting_factory(language=safe_environ("INPUT_LANGUAGE"))

        generate_path = os.path.join(repo.workdir, safe_environ("INPUT_PATH"))

        # Generate
        with change_workdir(generate_path), open("README.md", "w") as fp:
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
            msg=f"BOT : {finish} contribution report",
            email=safe_environ("INPUT_AUTHOR_EMAIL"),
            name=safe_environ("INPUT_AUTHOR_NAME"),
        )
        repo.push()

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
