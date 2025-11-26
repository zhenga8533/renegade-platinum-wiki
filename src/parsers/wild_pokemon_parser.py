"""
Parser for Wild Pokémon documentation file.

This parser:
1. Reads data/documentation/Wild Pokemon.txt
2. Generates a markdown file to docs/reference/wild_pokemon.md
"""

import re

from src.utils.core.loader import PokeDBLoader
from src.utils.formatters.markdown_formatter import format_pokemon, format_type_badge

from .base_parser import BaseParser


class WildPokemonParser(BaseParser):
    """Parser for Wild Pokémon documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/reference"):
        """Initialize the Wild Pokémon parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/reference".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Changes", "Area Changes"]

        # Constant States
        self._fishing_levels = {
            "Old Rod": "10",
            "Good Rod": "25",
            "Super Rod": "50",
        }
        self._method_map = {
            "Morning": "Walking",
            "Day": "Walking",
            "Night": "Walking",
            "Poké Radar": "Walking",
            "Surf": "Surfing",
        }

        # Area Changes States
        self._levels = {}

    def parse_general_changes(self, line: str) -> None:
        """Parse a line from the General Changes section.

        Args:
            line (str): A line from the General Changes section.
        """
        self.parse_default(line)

    def parse_area_changes(self, line: str) -> None:
        """Parse a line from the Area Changes section.

        Args:
            line (str): A line from the Area Changes section.
        """
        next_line = self.peek_line(1) or ""

        if next_line.startswith("Levels:"):
            self._markdown += f"### {line}\n\n"
        elif line.startswith("Levels:"):
            levels = line.split(": ")
            if len(levels) < 2:
                self.logger.warning(f"Could not parse levels from line: '{next_line}'")
                return

            # Parse levels
            for level in levels[1].split(", "):
                if match := re.match(r"^(.+?) \((.+?)\)$", level):
                    self._levels[match.group(2)] = match.group(1)
                else:
                    self._levels["Walking"] = level
        elif match := re.match(r"^(.+?)\s{2,}(.+?)$", line):
            method, pokemon = match.groups()
            encounters = pokemon.split(", ")
            self._markdown += self._format_wild_pokemon(method, encounters)
        else:
            self.parse_default(line)

    def _format_wild_pokemon(self, method: str, encounters: list[str]) -> str:
        """Format wild Pokémon data into markdown.

        Args:
            method (str): The method of encountering the Pokémon.
            encounters (list[str]): List of Pokémon names and their encounter chances.

        Returns:
            str: Formatted markdown string.
        """
        # Format header
        md = f"#### {method}\n\n"
        md += "| Pokémon | Type(s) | Level(s) | Chance |\n"
        md += "|:-------:|:-------:|:---------|:-------|\n"

        # Determine level range
        level_range = self._levels.get(self._method_map.get(method, method), "Unknown")
        if method in self._fishing_levels:
            level_range = self._fishing_levels[method]
        elif level_range == "Unknown":
            self.logger.warning(
                f"Unknown method '{method}' encountered with encounters '{encounters}'."
            )

        # Format each Pokémon entry
        has_encounters = False
        for pokemon in encounters:
            if match := re.match(r"^(.+?) \((\d+)%\)$", pokemon):
                name, chance = match.groups()
            else:
                self.logger.warning(
                    f"Could not parse encounter '{pokemon}' in method '{method}' with encounters '{encounters}'."
                )
                continue

            # Load Pokémon data
            pokemon_data = PokeDBLoader.load_pokemon(name)
            if pokemon_data is None:
                self.logger.warning(
                    f"Could not load data for Pokémon '{name}' in method '{method}' with encounters '{encounters}'."
                )
                continue
            pokemon_md = format_pokemon(pokemon_data)

            # Format types with badges
            types = pokemon_data.types
            type_badges = " ".join([format_type_badge(t) for t in types])
            type_html = f"<div class='badges-vstack'>{type_badges}</div>"

            md += f"| {pokemon_md} | {type_html} | {level_range} | {chance}% |\n"
            has_encounters = True

        return md + "\n" if has_encounters else ""
