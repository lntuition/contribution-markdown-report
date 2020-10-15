from unittest.mock import MagicMock

from src.markdown import MarkdownGraphSection, MarkdownHeaderSection, MarkdownSectionBuilder, MarkdownSummarySection


class TestMarkdownSectionBuilder:
    def test_build_header(self) -> None:
        setting = MagicMock()

        section_builder = MarkdownSectionBuilder(setting=setting)
        header = section_builder.build_header()

        assert isinstance(header, MarkdownHeaderSection)
        assert header.setting == setting

    def test_build_summary(self) -> None:
        setting = MagicMock()

        section_builder = MarkdownSectionBuilder(setting=setting)
        summary = section_builder.build_summary()

        assert isinstance(summary, MarkdownSummarySection)
        assert summary.setting == setting

    def test_build_graph(self) -> None:
        setting = MagicMock()

        section_builder = MarkdownSectionBuilder(setting=setting)
        graph = section_builder.build_graph()

        assert isinstance(graph, MarkdownGraphSection)
        assert graph.setting == setting
