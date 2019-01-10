import re

from reformat_money.match import TextMatch


class TextFormatter:
    """Formats the amount using simple regex to determine the starting type."""
    amount_as_string = re.compile(r"^[\"\'](?P<integral>\d+)\.?(?P<decimal>\d*)[\"\']$")  # matches ("120.00", "120", '493.23', '392')
    amount_as_integer = re.compile(r"^(?P<integral>[0-9]+)$")  # matches: (100, 200, 593)
    amount_as_float = re.compile(r"^(?P<integral>\d+)\.(?P<decimal>\d*)$")  # matches: (100., 100.3, 200.32, etc.)

    def __init__(self, match: TextMatch):
        self._match = match
        self._func = self._null_operator

    def match_string_representation(self):
        # Example: Money("1002.39", "GBP")
        found = self.amount_as_string.search(self._match.get_amount())
        if found:
            self._func = self.reformat_string
        return found

    def match_integer_representation(self):
        # Example: Money(200, "GBP")
        found = self.amount_as_integer.search(self._match.get_amount())
        if found:
            self._func = self.reformat_integer
        return found

    def match_float_representation(self):
        # Example: Money(203.23, "GBP")
        found = self.amount_as_float.search(self._match.get_amount())
        if found:
            self._func = self.reformat_float
        return found

    def reformat(self):
        self._inner_match = (
            self.match_string_representation()
            or self.match_integer_representation()
            or self.match_float_representation()
        )

    def _null_operator(self):
        # Method that just doesn't do anything (fun).
        pass

    def reformat_string(self):
        integral = self._inner_match.group("integral")
        decimal = self._inner_match.group("decimal")
        reformatted = self._build_reformatted_amount(integral, decimal)
        self._match.update_amount(reformatted)

    def reformat_integer(self):
        integral = self._inner_match.group("integral")
        reformatted = self._build_reformatted_amount(integral)
        self._match.update_amount(reformatted)

    def reformat_float(self):
        integral = self._inner_match.group("integral")
        decimal = self._inner_match.group("decimal")
        reformatted = self._build_reformatted_amount(integral, decimal)
        self._match.update_amount(reformatted)

    def _build_reformatted_amount(self, integral: str, decimal: str = "00"):
        """Ensure that we have at least 2 decimal places for consistency."""
        while len(decimal) < 2:
            decimal += "0"
        return f'"{integral}.{decimal}"'

    def get_reformatted(self):
        self._func()
        return str(self._match)

    def span(self):
        return (self._match.start, self._match.stop)

    @property
    def able_to_format(self) -> bool:
        return bool(self._inner_match)
