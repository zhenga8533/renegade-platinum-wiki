"""
Parser for Special Events documentation file.

This parser:
1. Reads data/documentation/SpecialEvents.txt
2. Generates a markdown file to docs/reference/special_events.md
"""

import re
from typing import Any

from renegade_platinum_wiki.utils.formatters.markdown_formatter import (
    format_pokemon_card_grid,
)

from .base_parser import BaseParser


class SpecialEventsParser(BaseParser):
    """Parser for Special Events documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/reference"):
        """Initialize the Special Events parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/reference".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Notes", "Gift Pokémon", "Legendary Encounters"]

    def parse_general_notes(self, line: str) -> None:
        """Parse a line from the General Notes section.

        Args:
            line (str): A line from the General Notes section.
        """
        self.parse_default(line)

    def parse_gift_pokemon(self, line: str) -> None:
        """Parse a line from the Gift Pokémon section.

        Args:
            line (str): A line from the Gift Pokémon section.
        """
        next_line = self.peek_line(1)

        # Matches: Next line is '---'
        if next_line == "---":
            self._markdown += f"### {line}\n"
            if not line.startswith("#"):
                return

            pokemon: list[str | Any] = [p.split(" ")[1] for p in line.split(", ")]
            self._markdown += f"\n{format_pokemon_card_grid(
                pokemon, relative_path='../pokedex/pokemon'
            )}\n"
        # Matches: '---'
        elif line == "---":
            self._markdown += "\n"
        # Matches: 'Key: Value'
        elif match := re.match(r"^(.*): (.*)$", line):
            key, value = match.groups()
            self._markdown += f"**{key}**: {value}\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_legendary_encounters(self, line: str) -> None:
        """Parse a line from the Legendary Encounters section.

        Args:
            line (str): A line from the Legendary Encounters section.
        """
        self.parse_gift_pokemon(line)
