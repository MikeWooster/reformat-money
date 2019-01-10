import pytest

from reformat_money.arguments import Argument


@pytest.mark.parametrize("original,leading_whitespace", [
    ("   argumentText", "   "),
    (" argumentText", " "),
    ("\nargumentText", "\n"),
    (" \n \n argumentText", " \n \n "),
])
def test_argument_strips_off_leading_whitespace(original, leading_whitespace):
    argument = Argument(original)
    assert argument.get_leading_whitespace() == leading_whitespace
    assert argument.get_text() == "argumentText"
    assert argument.get_trailing_whitespace() == ""


@pytest.mark.parametrize("original,trailing_whitespace", [
    ("argumentText   ", "   "),
    ("argumentText ", " "),
    ("argumentText\n", "\n"),
    ("argumentText \n \n ", " \n \n "),
])
def test_argument_strips_off_trailing_whitespace(original, trailing_whitespace):
    argument = Argument(original)
    assert argument.get_leading_whitespace() == ""
    assert argument.get_text() == "argumentText"
    assert argument.get_trailing_whitespace() == trailing_whitespace


@pytest.mark.parametrize("original,whitespace", [
    ("   argumentText   ", "   "),
    (" argumentText ", " "),
    ("\nargumentText\n", "\n"),
    (" \n \n argumentText \n \n ", " \n \n "),
])
def test_argument_strips_off_leading_and_trailing_whitespace(original, whitespace):
    argument = Argument(original)
    assert argument.get_leading_whitespace() == whitespace
    assert argument.get_text() == "argumentText"
    assert argument.get_trailing_whitespace() == whitespace


@pytest.mark.parametrize("original", [
    "   argumentText   ",
    " argumentText ",
    "\nargumentText\n",
    " \n \n argumentText \n \n ",
])
def test_argument_string_method_returns_original_when_not_changed(original):
    argument = Argument(original)
    assert str(argument) == original


@pytest.mark.parametrize("original,expected", [
    ("   argumentText   ", "   newText   "),
    (" argumentText ", " newText "),
    ("\nargumentText\n", "\nnewText\n"),
    (" \n \n argumentText \n \n ", " \n \n newText \n \n "),
])
def test_argument_string_method_returns_updated_when_text_set(original, expected):
    argument = Argument(original)
    assert argument.get_text() == "argumentText"
    argument.set_text("newText")
    assert argument.get_text() == "newText"
    assert str(argument) == expected


def test_repr():
    argument = Argument("foo")
    assert repr(argument) == "'foo'"
