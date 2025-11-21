"""
Parser for Trade Changes documentation file.

This parser:
1. Reads data/documentation/Trade Changes.txt
2. Generates a markdown file to docs/trade_changes.md
"""

import re

from .base_parser import BaseParser


class TradeChangesParser(BaseParser):
    """Parser for Trade Changes documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs"):
        """Initialize the Trade Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Changes"]

    def parse_general_changes(self, line: str) -> None:
        """Parse a line from the General Changes section.

        Args:
            line (str): A line from the General Changes section.
        """
        next_line = self.peek_line(1)

        # Matches: Next line is '---'
        if next_line == "---":
            self._markdown += f"### {line}\n"
        # Matches: '---'
        elif line == "---":
            self._markdown += "\n"
        elif match := re.match(r"^(\w+) the (\w+)$", line):
            nickname, pokemon = match.groups()
        elif match := re.match(
            r"^You will be asked for a (\w+) in exchange for a (.+?).$", line
        ):
            give, receive = match.groups()
        elif match := re.match("^- (\w+): (.+?)$", line):
            key, value = match.groups()
        # Default: regular text line
        else:
            self.parse_default(line)
