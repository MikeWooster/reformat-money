import re
from typing import List

from reformat_money.match import TextMatch
from reformat_money.text_formatter import TextFormatter


class FileFormatter:
    SEARCH_PATTERN = re.compile(r"Money\(")
    REFORMAT_PATTERN = re.compile(r"(?P<class_name>Money)\((?P<contents>.*[\"\']\w{3}[\"\'])\)")
    CLOSING_BRACKET = ")"
    OPENING_BRACKET = "("
    QUOTES = {"'", '"',}
    ESCAPE = "\\"
    COMMA = ","

    def __init__(self, file):
        self._file = file
        self._total_matches = 0
        self._formatted = 0
        self._unable_to_format = 0

    def reformat(self):
        with open(self._file, 'r') as buf:
            self.set_contents(buf.read())

        self.find_and_reformat_matches()

        with open(self._file, 'w') as buf:
            buf.write(self.get_contents())

    def set_contents(self, contents: str):
        self._contents_str = contents
        self._contents = list(contents)
        self._file_characters = len(self._contents)

    def get_contents(self) -> str:
        return "".join(self._contents)

    def find_and_reformat_matches(self):
        for match in self.find_matches():
            self._reformat_match(match)
        self._maybe_print_summary()

    def find_matches(self) -> List[TextMatch]:
        """Returns list of matches.

        Matches are returned in the reverse order that
        they appear in file.
        """
        matches = []
        for match in self.SEARCH_PATTERN.finditer(self._contents_str):
            self._total_matches += 1
            start = match.end()
            text_match = self.split_args(start)
            matches.append(text_match)
        return matches[::-1]

    def split_args(self, start: int) -> TextMatch:
        inspect = True
        opening_quote = "'"
        opening_bracket_count = 1
        closing_bracket_count = 0
        argument_start_positions = []
        stop = None

        for i in range(start, self._file_characters):
            char = self._contents[i]
            prev_char = self._contents[i - 1] if i >= 1 else None
            # Ignore everything that appears within quotes.
            # TODO: handle triple quotes
            if inspect and char in self.QUOTES:
                opening_quote = char
                inspect = False
                continue
            if not inspect and char == opening_quote and prev_char != self.ESCAPE:
                inspect = True
                continue
            if inspect and char == self.OPENING_BRACKET:
                opening_bracket_count += 1
            if inspect and (opening_bracket_count - closing_bracket_count) == 1 and char == self.COMMA:
                # This denotes a new argument starting
                argument_start_positions.append(i)
            if inspect and char == self.CLOSING_BRACKET:
                closing_bracket_count += 1
                if closing_bracket_count == opening_bracket_count:
                    # Stop position should not include the closing bracket.
                    stop = i - 1
                    break
        if stop is None:
            raise RuntimeError(f"Unable to find closing bracket for start position '{start}'")
        if argument_start_positions:
            # Append the last position so that we include the last argument too.
            # As we will be using slicing, we need to increment stop by one.
            argument_start_positions.append(stop+1)
            match = TextMatch(
                args=self._get_arguments_from_start_positions(start, argument_start_positions),
                start=start,
                stop=stop,
            )
        else:
            match = TextMatch(
                args=["".join(self._contents[start: stop+1])],
                start=start,
                stop=stop,
            )
        return match

    def _get_arguments_from_start_positions(self, last_pos: int, positions: list) -> List[str]:
        args = []
        for pos in positions:
            args.append("".join(self._contents[last_pos: pos]))
            last_pos = pos + 1
        return args

    def _reformat_match(self, match: TextMatch):
        original_amount = match.get_amount()
        formatter = TextFormatter(match)
        formatter.reformat()

        self._update(formatter)

        if not formatter.able_to_format:
            self._unable_to_format += 1
        elif original_amount != match.get_amount():
            self._formatted += 1

    def _maybe_print_summary(self):
        if self._total_matches and self._unable_to_format == 0 and self._formatted > 0:
            print(f"{self._file} -- Reformatted: {self._formatted}")
        elif self._total_matches and self._unable_to_format > 0:
            print(f"{self._file} -- Reformatted: {self._formatted}, Unable to reformat: {self._unable_to_format}")

    def _update(self, formatter: TextFormatter):
        start, end = formatter.span()
        new_string = formatter.get_reformatted()
        del (self._contents[start:end+1])
        pos = start
        for i, char in enumerate(new_string):
            self._contents.insert(pos+i, char)
