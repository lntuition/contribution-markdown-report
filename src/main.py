import os
import sys

from data import (
    append_csv_data,
    generate_csv_data,
    generate_markdown_table
)
from request import request_github_commit


DATA_PATH = "result/data.csv"
TABLE_PATH = "result/README.md"

if __name__ == "__main__":
    config = {
        "username": sys.argv[1],
        "start-date": sys.argv[2],
        "target-date": sys.argv[3],
    }

    commit_data = request_github_commit(
        username=config["username"]
    )

    if not os.path.exists(DATA_PATH):
        generate_csv_data(
            start=config["start-date"],
            target=config["target-date"],
            path=DATA_PATH,
            commits=commit_data
        )

    append_csv_data(
        target=config["target-date"],
        path=DATA_PATH,
        commits=commit_data
    )

    generate_markdown_table(
        data_path=DATA_PATH,
        table_path=TABLE_PATH
    )
