from typing import Any, Dict

from base.crawler import CrawledDataType
from report.section.graph import GraphGenerator
from report.section.header import HeaderGenerator
from report.section.summary import SummaryGenerator
from report.section.table import TableGenerator

ConfigType = Dict[str, Any]


class BaseReportManager(GraphGenerator, HeaderGenerator, SummaryGenerator, TableGenerator, ):
    def generate(self, username: str, data: CrawledDataType) -> None:
        with open("result/README.md", "w") as md:
            md.write(self.generate_header(username=username))
            md.write(self.generate_summary(data=data))
            md.write(self.generate_graph(data=data))
            md.write(self.generate_table(data=data))
