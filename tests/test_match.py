import pytest

from reformat_money.match import TextMatch


def test_text_match_string_method():
    match = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    assert str(match) == "foo,bar"


def test_text_match_repr_method():
    match = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    assert repr(match) == f"TextMatch(args=['foo', 'bar'], start=0, stop=10)"


def test_text_match_equality_with_same_types():
    match1 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    match2 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    assert match1 == match2


def test_text_match_equality_with_same_object():
    match = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    assert match == match

@pytest.mark.parametrize("args", [
    ["DIFF", "bar"],
    ["foo", "DIFF"],
    [],
    ["foo"],
    ["bar"],
    ["DIFF", "DIFF"],
    ["foo", "bar", "NEW"],
    ["DIFF", "DIFF", "NEW"],
])
def test_text_match_inequality_when_args_are_different(args):
    match1 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    match2 = TextMatch(
        args=args,
        start=0,
        stop=10,
    )
    assert match1 != match2


@pytest.mark.parametrize("start", [
    -1,
    1,
    None,
    0.0,
    1.0,
    "foo",
])
def test_text_match_inequality_when_start_is_different(start):
    match1 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    match2 = TextMatch(
        args=["foo", "bar"],
        start=start,
        stop=10,
    )
    assert match1 != match2


@pytest.mark.parametrize("stop", [
    9,
    11,
    None,
    10.0,
    11.0,
    "foo",
])
def test_text_match_inequality_when_stop_is_different(stop):
    match1 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    match2 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=stop,
    )
    assert match1 != match2


def test_text_match_inequality_when_different_type():
    match1 = TextMatch(
        args=["foo", "bar"],
        start=0,
        stop=10,
    )
    match2 = "string"
    assert match1 != match2


@pytest.mark.parametrize("amount", [
    "foo",
    " foo ",
    "\nfoo\n",
])
def test_update_and_get_amount(amount):
    match = TextMatch(
        args=[amount, "bar"],
        start=0,
        stop=10,
    )
    assert match.get_amount() == "foo"
    match.update_amount("NEW")
    assert match.get_amount() == "NEW"
