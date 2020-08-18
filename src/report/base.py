from pandas import DataFrame

from report.section.graph import GraphGenerator
from report.section.header import HeaderGenerator
from report.section.summary import SummaryGenerator


class BaseReportManager(GraphGenerator, HeaderGenerator, SummaryGenerator):
    def generate(self, username: str, data: DataFrame) -> None:
        root_path = "result"
        asset_dir = "asset"
        report_file = "README.md"

        with open(f"{root_path}/{report_file}", "w") as md:
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
                    root_path=root_path,
                    asset_dir=asset_dir,
                )
            )
