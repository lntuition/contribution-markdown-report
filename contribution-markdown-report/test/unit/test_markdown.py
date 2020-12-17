import pytest

from src.markdown import Markdown


def test_default_style() -> None:
    markdown = Markdown(expr="one")

    assert "one\n" == str(markdown)


def test_single_fmt() -> None:
    markdown = Markdown(
        expr="{first}.for",
        fmt={
            "first": "one",
        },
    )

    assert "one.for\n" == str(markdown)


def test_double_fmt() -> None:
    markdown = Markdown(
        expr="{first}.for.{second}",
        fmt={
            "first": "one",
            "second": "two",
        },
    )

    assert "one.for.two\n" == str(markdown)


def test_nested_fmt() -> None:
    markdown = Markdown(
        expr="{first}.for",
        fmt={
            "first": Markdown(expr="1"),
        },
    )

    assert "1\n.for\n" == str(markdown)


def test_deep_nested_fmt() -> None:
    inner_markdown = Markdown(
        expr="{second}.to",
        fmt={
            "second": "two",
        },
    )

    markdown = Markdown(
        expr="{first}.for",
        fmt={
            "first": inner_markdown,
        },
    )

    assert "two.to\n.for\n" == str(markdown)


def test_not_enough_fmt() -> None:
    markdown = Markdown(
        expr="{first}.for.{second}",
        fmt={
            "first": "one",
        },
    )

    with pytest.raises(Exception):
        str(markdown)


def test_wrong_fmt() -> None:
    markdown = Markdown(
        expr="{first}.for",
        fmt={
            "fist": "one",
        },
    )

    with pytest.raises(Exception):
        str(markdown)


def test_change_end() -> None:
    markdown = Markdown(expr="one", end="")

    assert "one" == str(markdown)


@pytest.mark.parametrize("level", [1, 2, 3, 4, 5])
def test_heading_right_level(level: int) -> None:
    markdown = Markdown(expr="one").to_heading(level=level)

    assert "#" * level + "one\n" == str(markdown)


@pytest.mark.parametrize("level", [0, 6])
def test_heading_wrong_level(level: int) -> None:
    with pytest.raises(Exception):
        Markdown(expr="one").to_heading(level=level)


def test_ordered_list() -> None:
    markdown = Markdown(expr="one").to_list(is_ordered=True)

    assert "1. one\n" == str(markdown)


def test_unordered_list() -> None:
    markdown = Markdown(expr="one").to_list(is_ordered=False)

    assert "- one\n" == str(markdown)


def test_blockquote() -> None:
    markdown = Markdown(expr="one").to_blockquote()

    assert ">one\n" == str(markdown)


def test_bold() -> None:
    markdown = Markdown(expr="one").to_bold()

    assert "**one**\n" == str(markdown)


def test_italic() -> None:
    markdown = Markdown(expr="one").to_italic()

    assert "*one*\n" == str(markdown)


def test_bold_next_italic() -> None:
    markdown = Markdown(expr="one").to_italic().to_bold()

    assert "***one***\n" == str(markdown)


def test_italic_next_bold() -> None:
    markdown = Markdown(expr="one").to_bold().to_italic()

    assert "***one***\n" == str(markdown)


def test_emoji() -> None:
    markdown = Markdown(expr="one").to_emoji()

    assert ":one:\n" == str(markdown)


def test_code() -> None:
    markdown = Markdown(expr="one").to_code()

    assert "`one`\n" == str(markdown)


def test_link_url() -> None:
    markdown = Markdown(expr="one").link_url(path="/url")

    assert "[one](/url)\n" == str(markdown)


def test_link_image() -> None:
    markdown = Markdown(expr="one").link_image(path="/image")

    assert "![one](/image)\n" == str(markdown)
