import os

from pandas import DataFrame

from report.section.graph import GraphGenerator
from report.section.header import HeaderGenerator
from report.section.summary import SummaryGenerator


class BaseReportManager(GraphGenerator, HeaderGenerator, SummaryGenerator):
    def generate(self, username: str, data: DataFrame, workdir: str) -> None:
        os.makedirs(workdir, exist_ok=True)
        os.chdir(workdir)

        with open("README.md", "w") as md:
            md.write(
                self.generate_header(
                    username=username
                )
            )
            md.write(
                self.generate_summary(
                    data=data
                )
            )
            md.write(
                self.generate_graph(
                    data=data,
                    workdir="asset"
                )
            )

        os.chdir("..")
