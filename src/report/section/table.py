import pytablewriter as ptw

from textwrap import dedent
from pytablewriter.style import Style as ptwStyle

from base.type import ConfigType, CrawledDataType


class TableGenerator():
    def _config_table(self) -> ConfigType:
        raise NotImplementedError()

    def generate_table(self, data: CrawledDataType) -> str:
        config = self._config_table()

        writer = ptw.MarkdownTableWriter()
        writer.headers = config["headers"]
        writer.table_name = None
        writer.column_styles = [ptwStyle(align="center")] * 8
        writer.margin = 1
        writer.value_matrix = []

        for dt, cnt in data.items():
            year, week, day = dt.isocalendar()
            formatted_dt = config["formatter"](year=year, week=week)

            if not writer.value_matrix or writer.value_matrix[-1][0] != formatted_dt:
                writer.value_matrix.append([formatted_dt] + [""] * 7)

            writer.value_matrix[-1][day] = cnt

        # pytablewriter dumps without front blank, so dedent doesn't work well
        return f"""
## Contribution table
{writer.dumps(flavor="github")}
        """
