from __future__ import annotations

from typing import Dict, Union


class MarkdownBuilder:
    def __init__(
        self,
        expr: str,
        fmt: Dict[str, Union[str, MarkdownBuilder]] = {},
        end: str = "\n",
    ) -> None:
        self.__expr = expr
        self.__fmt = fmt
        self.__wrapper = "{}"
        self.__end = end

    def __repr__(self) -> str:
        try:
            self.__expr = self.__expr.format(**self.__fmt)
        except KeyError as e:
            raise Exception("Not enough or wrong fmt key") from e

        wrapped = self.__wrapper.format(self.__expr)

        return wrapped + self.__end

    def to_heading(self, level: int) -> MarkdownBuilder:
        if level < 1 or level > 5:
            raise Exception("level must be between 1 and 5")
        self.__wrapper = "#" * level + " " + self.__wrapper

        return self

    def to_list(self, is_ordered: bool) -> MarkdownBuilder:
        if is_ordered:
            self.__wrapper = "1. " + self.__wrapper
        else:
            self.__wrapper = "- " + self.__wrapper

        return self

    def to_blockquote(self) -> MarkdownBuilder:
        self.__wrapper = ">" + self.__wrapper

        return self

    def __wrap_wrapper_and_return_self(self, s: str) -> MarkdownBuilder:
        self.__wrapper = s + self.__wrapper + s
        return self

    def to_bold(self) -> MarkdownBuilder:
        return self.__wrap_wrapper_and_return_self("**")

    def to_italic(self) -> MarkdownBuilder:
        return self.__wrap_wrapper_and_return_self("*")

    def to_emoji(self) -> MarkdownBuilder:
        return self.__wrap_wrapper_and_return_self(":")

    def to_code(self) -> MarkdownBuilder:
        return self.__wrap_wrapper_and_return_self("`")

    def __link_wrapper_with_link(self, path: str) -> None:
        self.__wrapper = "[" + self.__wrapper + "]" + "(" + path + ")"

    def link_url(self, path: str) -> MarkdownBuilder:
        self.__link_wrapper_with_link(path)

        return self

    def link_image(self, path: str) -> MarkdownBuilder:
        self.__link_wrapper_with_link(path)
        self.__wrapper = "!" + self.__wrapper

        return self
