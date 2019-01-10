

class Argument:
    """Parses a python argument as string.

    All whitespace before and after the argument text itself
    is stripped off and saved for later reformatting.

    """

    def __init__(self, original: str):
        original.lstrip()
        start = 0
        end = len(original) - 1
        while original[start].isspace():
            start += 1
        while original[end].isspace():
            end -= 1
        # End requires +1 when used in string slicing.
        end += 1
        self._leading_whitespace = original[:start]
        self._trailing_whitespace = original[end:]
        self.set_text(original[start:end or None])

    def get_leading_whitespace(self):
        return self._leading_whitespace

    def get_trailing_whitespace(self):
        return self._trailing_whitespace

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def __str__(self):
        return f"{self.get_leading_whitespace()}{self.get_text()}{self.get_trailing_whitespace()}"

    def __repr__(self):
        return f"'{self}'"

    def __eq__(self, other):
        return (
            isinstance(other, Argument) and
            self.get_leading_whitespace() == other.get_leading_whitespace() and
            self.get_text() == other.get_text() and
            self.get_trailing_whitespace() == other.get_trailing_whitespace()
        )