import re

import pytest

from reformat_money.match import TextMatch
from reformat_money.text_formatter import TextFormatter


def get_match(*args):
    stop = len(" ".join(args))
    return TextMatch(args=args, start=0, stop=stop)


@pytest.mark.parametrize("input_string", [
    '"3930.39"',
    '"1023"',
    '"102."',
    '"382.1"',
])
def test_match_string_representation(input_string):
    match = get_match(input_string, '"GBP"')
    formatter = TextFormatter(match)

    assert bool(formatter.match_string_representation()) is True
    assert bool(formatter.match_integer_representation()) is False
    assert bool(formatter.match_float_representation()) is False


@pytest.mark.parametrize("input_string", [
    '100',
    ' 100',
    '  100',
    '99999',
    '0',
    '00192',
])
def test_match_integer_representation(input_string):
    match = get_match(input_string, ' "GBP"')
    formatter = TextFormatter(match)
    assert bool(formatter.match_integer_representation()) is True

    assert bool(formatter.match_string_representation()) is False
    assert bool(formatter.match_float_representation()) is False


@pytest.mark.parametrize("input_string", [
    '100.92',
    ' 100.92',
    '100.9202',
    '100.9',
    '100.',
    ' 100.',
])
def test_match_float_representation(input_string):
    match = get_match(input_string, ' "GBP"')
    formatter = TextFormatter(match)
    assert bool(formatter.match_float_representation()) is True

    assert bool(formatter.match_integer_representation()) is False
    assert bool(formatter.match_string_representation()) is False


@pytest.mark.parametrize("input_string,expected", [
    ('100.92', '"100.92", "GBP"'),
    (' 100.92', ' "100.92", "GBP"'),
    ('100.9202', '"100.9202", "GBP"'),
    ('100.9', '"100.90", "GBP"'),
    ('100.', '"100.00", "GBP"'),
    (' 100.', ' "100.00", "GBP"'),
    ('\n   100.', '\n   "100.00", "GBP"'),
])
def test_reformat_float(input_string, expected):
    match = get_match(input_string, ' "GBP"')
    formatter = TextFormatter(match)
    formatter.reformat()
    assert formatter.get_reformatted() == expected


@pytest.mark.parametrize("input_string,expected", [
    ('100', '"100.00", "GBP"'),
    (' 100', ' "100.00", "GBP"'),
    ('\n100', '\n"100.00", "GBP"'),
    ('\n    100', '\n    "100.00", "GBP"'),
    ('\n\n100', '\n\n"100.00", "GBP"'),
    ('   100', '   "100.00", "GBP"'),
    ('0', '"0.00", "GBP"'),
])
def test_reformat_integer(input_string, expected):
    match = get_match(input_string, ' "GBP"')
    formatter = TextFormatter(match)
    formatter.reformat()
    assert formatter.get_reformatted() == expected


@pytest.mark.parametrize("input_string,expected", [
    ('"3930.39"', '"3930.39", "GBP"'),
    ('"1023"', '"1023.00", "GBP"'),
    ('"102."', '"102.00", "GBP"'),
    ('"382.1"', '"382.10", "GBP"'),
])
def test_reformat_string(input_string, expected):
    match = get_match(input_string, ' "GBP"')
    formatter = TextFormatter(match)
    formatter.reformat()
    assert formatter.get_reformatted() == expected


def test_get_reformatted_with_no_match_does_nothing():
    match = get_match("max([10.00, 20.00])", " 'GBP'")
    formatter = TextFormatter(match)
    formatter.reformat()
    assert formatter.get_reformatted() == "max([10.00, 20.00]), 'GBP'"
