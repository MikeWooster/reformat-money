from io import StringIO
from unittest.mock import patch

import pytest

from reformat_money.file_formatter import FileFormatter, TextMatch


def test_file_formatter():
    text = "              amount=Money(20000, 'GBP'), amount_available=Money(1900, 'GBP')),), ],"
    formatter = FileFormatter("filename.txt")
    formatter.set_contents(text)
    formatter.find_and_reformat_matches()
    expected = "              amount=Money(\"20000.00\", 'GBP'), amount_available=Money(\"1900.00\", 'GBP')),), ],"
    assert formatter.get_contents() == expected


@pytest.mark.parametrize("actual,expected", [
    ("foo bar Money('200.00', 'GBP') bar foo", TextMatch(args=["'200.00'", " 'GBP'"], start=14, stop=28)),
    ("Money('200.00', 'GBP')", TextMatch(args=["'200.00'", " 'GBP'"], start=6, stop=20)),
    ("Money('200.00foo)', 'GBP')", TextMatch(args=["'200.00foo)'", " 'GBP'"], start=6, stop=24)),
    ("""Money('200.00"foo"', 'GBP')""", TextMatch(args=["""'200.00"foo"'""", " 'GBP'"], start=6, stop=25)),
    ("Money(Decimal(100), 'GBP')", TextMatch(args=["Decimal(100)", " 'GBP'"], start=6, stop=24)),
    ("Money(\n'    200.00',\n    'GBP')", TextMatch(args=["\n'    200.00'", "\n    'GBP'"], start=6, stop=29)),
    ('Money("190.92", "GBP")', TextMatch(args=['"190.92"', ' "GBP"'], start=6, stop=20)),
    ("Money(200.19, 'GBP')", TextMatch(args=["200.19", " 'GBP'"], start=6, stop=18)),
    ("Money(290, 'GBP')", TextMatch(args=["290", " 'GBP'"], start=6, stop=15)),
    ("Money(290)", TextMatch(args=["290"], start=6, stop=8)),
])
def test_find_matches(actual, expected):
    formatter = FileFormatter('filename.txt')
    formatter.set_contents(actual)
    matches = formatter.find_matches()
    assert len(matches) == 1
    assert matches[0] == expected


def test_find_matches_multiple_occurances_one_line():
    text = "              amount=Money(20000, 'GBP'), amount_available=Money(20000, 'GBP')),), ],"
    formatter = FileFormatter("filename.txt")
    formatter.set_contents(text)
    matches = formatter.find_matches()
    assert len(matches) == 2
    assert matches[0] == TextMatch(args=["20000", " 'GBP'"], start=65, stop=76)
    assert matches[1] == TextMatch(args=["20000", " 'GBP'"], start=27, stop=38)


def test_matches_are_returned_in_reverse_order():
    actual = "Money(290, 'GBP')Money(823091, 'GBP')"
    formatter = FileFormatter('filename.txt')
    formatter.set_contents(actual)
    matches = formatter.find_matches()
    assert len(matches) == 2
    assert matches[0] == TextMatch(args=["823091", " 'GBP'"], start=23, stop=35)
    assert matches[1] == TextMatch(args=["290", " 'GBP'"], start=6, stop=15)


@pytest.mark.parametrize("actual,expected", [
    ("foo bar Money('200.00', 'GBP') bar foo", TextMatch(args=["'200.00'", " 'GBP'"], start=14, stop=28)),
    ("Money('200.00', 'GBP')", TextMatch(args=["'200.00'", " 'GBP'"], start=6, stop=20)),
    ("Money('200.00foo)', 'GBP')", TextMatch(args=["'200.00foo)'", " 'GBP'"], start=6, stop=24)),
    ("""Money('200.00"foo"', 'GBP')""", TextMatch(args=["""'200.00"foo"'""", " 'GBP'"], start=6, stop=25)),
    ("Money(Decimal(100), 'GBP')", TextMatch(args=["Decimal(100)", " 'GBP'"], start=6, stop=24)),
    ("Money(\n'    200.00',\n    'GBP')", TextMatch(args=["\n'    200.00'", "\n    'GBP'"], start=6, stop=29)),
    ('Money("190.92", "GBP")', TextMatch(args=['"190.92"', ' "GBP"'], start=6, stop=20)),
    ("Money(200.19, 'GBP')", TextMatch(args=["200.19", " 'GBP'"], start=6, stop=18)),
    ("Money(290, 'GBP')", TextMatch(args=["290", " 'GBP'"], start=6, stop=15)),
    ("Money(290)", TextMatch(args=["290"], start=6, stop=8)),
])
def test_split_args(actual, expected):
    formatter = FileFormatter('filename.txt')
    formatter.set_contents(actual)
    match = formatter.split_args(expected.start)
    assert len(match.args) == len(expected.args)
    assert match == expected


def test_split_args_cannot_find_matching_bracket():
    formatter = FileFormatter('filename.txt')
    formatter.set_contents("Money(foo")
    with pytest.raises(RuntimeError) as exc_info:
        formatter.split_args(6)
    assert str(exc_info.value) == "Unable to find closing bracket for start position '6'"


def test_unable_to_format_prints_message(capsys):
    formatter = FileFormatter('filename.txt')
    formatter.set_contents("Money(max([1,2,3]))")
    formatter.find_and_reformat_matches()
    captured = capsys.readouterr()
    assert "filename.txt -- Reformatted: 0, Unable to reformat: 1" in captured.out


def test_reformatting_prints_message(capsys):
    formatter = FileFormatter('filename.txt')
    formatter.set_contents("Money(10.02, 'GBP')")
    formatter.find_and_reformat_matches()
    captured = capsys.readouterr()
    assert "filename.txt -- Reformatted: 1" in captured.out


def test_no_changes_when_formatting_does_not_print_message(capsys):
    formatter = FileFormatter('filename.txt')
    formatter.set_contents('Money("10.02", "GBP")')
    formatter.find_and_reformat_matches()
    captured = capsys.readouterr()
    assert "filename.txt -- Reformatted:" not in captured.out


@patch("reformat_money.file_formatter.open")
@patch("reformat_money.file_formatter.FileFormatter.find_and_reformat_matches")
def test_reformat(mock_find_and_reformat_matches, mock_open):
    # Test mainly for coverage...
    formatter = FileFormatter('filename.txt')
    formatter.reformat()
    assert mock_open.call_count == 2
    assert mock_find_and_reformat_matches.call_count == 1
