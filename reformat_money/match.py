from typing import List

from reformat_money.arguments import Argument


class TextMatch:
    def __init__(self, args: List[str], start: int, stop: int):
        self.args: List[Argument] = [Argument(arg) for arg in args]
        self.start: int = start
        self.stop: int = stop

    def __str__(self):
        return ",".join([str(arg) for arg in self.args])

    def __repr__(self):
        return f"TextMatch(args={self.args}, start={self.start}, stop={self.stop})"

    def __eq__(self, other):
        return (
            isinstance(other, TextMatch) and
            self.args == other.args and
            self.start is other.start and
            self.stop is other.stop
        )

    def update_amount(self, amount: str):
        self.args[0].set_text(amount)

    def get_amount(self):
        return self.args[0].get_text()
