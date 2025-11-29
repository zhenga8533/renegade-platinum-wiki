"""
Parser for Trade Changes documentation file.

This parser:
1. Reads data/documentation/Trade Changes.txt
2. Generates a markdown file to docs/changes/trade_changes.md
"""

import re

from src.utils.formatters.markdown_formatter import (
    format_pokemon,
    format_pokemon_card_grid,
)

from .base_parser import BaseParser


class TradeChangesParser(BaseParser):
    """Parser for Trade Changes documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/changes"):
        """Initialize the Trade Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/changes".
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
            self._markdown += f"### {line}\n\n"
        # Matches: '---'
        elif line == "---":
            self._markdown += "\n"
        # Matches: "You will be asked for a X in exchange for a Y."
        elif match := re.match(
            r"^You will be asked for a (.+?) in exchange for a (.+?)\.$", line
        ):
            give, receive = match.groups()

            # Format the exchange text with Pokemon links
            give_formatted = format_pokemon(give, has_sprite=False)
            receive_formatted = format_pokemon(receive, has_sprite=False)

            self._markdown += f"You will be asked for a {give_formatted} in exchange for a {receive_formatted}.\n\n"
        # Matches: "Nickname the Pokemon"
        elif match := re.match(r"^(\w+) the (.+?)$", line):
            nickname, pokemon = match.groups()
            self._markdown += format_pokemon_card_grid(
                [pokemon],
                extra_info=[f"*{nickname}*"],
                relative_path="../pokedex/pokemon",
            )
        # Matches: "- Key: Value"
        elif match := re.match(r"^- (.+?): (.+?)$", line):
            key, value = match.groups()
            self._markdown += f"- **{key}**: {value}\n"
        # Default: regular text line
        else:
            self.parse_default(line)
