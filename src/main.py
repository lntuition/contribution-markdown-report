import os
import sys

from data import DataManager

if __name__ == "__main__":
    data = DataManager(
        username=sys.argv[1],
        start=sys.argv[2],
        end=sys.argv[3],
    )

    data.generate_report(save_path="result/README.md")
