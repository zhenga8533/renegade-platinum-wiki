"""
Parser for Trainer Pokémon documentation file.

This parser:
1. Reads data/documentation/Trainer Pokemon.txt
2. Generates a markdown file to docs/reference/trainer_pokemon.md
"""

import re

from src.utils.formatters.markdown_formatter import (
    format_ability,
    format_item,
    format_move,
    format_pokemon,
    format_pokemon_card_grid,
)

from .base_parser import BaseParser


class TrainerPokemonParser(BaseParser):
    """Parser for Trainer Pokémon documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/reference"):
        """Initialize the Trainer Pokémon parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/reference".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Changes", "Area Changes"]

        # Area Changes States
        self._category = None
        self._current_trainer = None
        self._current_team = []

        # Example Structure: {'Normal Trainers': {'Name': {'Default': [team]}}, ...}
        self._trainers = {}

    def _set_category(self, category: str) -> None:
        """Set the current category for trainers.

        Args:
            category (str): The category to set.
        """
        if category not in self._trainers:
            self._trainers[category] = {}
        self._category = category

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

        # Matches: Header section
        if next_line == "---":
            self._markdown += self._format_trainers()
            self._trainers = {}

            self._markdown += f"### {line}\n\n"
            self._set_category("Normal Trainers")
        elif line == "---":
            pass
        # Matches: Pokémon (Lv. XX) @ Item / Nature / Ability / Move1, Move2, Move3, Move4
        elif match := re.match(
            r"^(.+?) \(Lv. (\d+)\) @ (.+?)/(.+?)/(.+?)/(.+?)$", line
        ):
            pokemon, level, item, nature, ability, moves = match.groups()
            item = item.strip()
            nature = nature.strip()
            ability = ability.strip()
            moves = moves.strip().split(", ")

            pokemon_md = format_pokemon(pokemon)
            item_md = format_item(item)
            moves_md = "<br>".join([format_move(move) for move in moves])
            ability_md = format_ability(ability)

            if len(self._current_team) == 0:
                self._current_team.append("| Pokémon | Attributes | Moves |")
                self._current_team.append("|:-------:|:-----------|:------|")
            self._current_team.append(
                f"| {pokemon_md} | **Level:** Lv. {level}<br>**Item:**{item_md}<br>**Nature:** {nature}<br>**Ability:** {ability_md}| {moves_md} |"
            )
        # Matches: Next line matches ^ (@)
        elif "@" in next_line:
            self._set_category("Important Trainers")
            self._current_trainer = line
            if self._current_trainer not in self._trainers[self._category]:
                self._trainers[self._category][self._current_trainer] = {}
        # Matches: Trainer Name  Team Pokémon, Team Pokémon, ...
        elif match := re.match(r"^(.+?)\s{2,}(.+)$", line):
            trainer, team = match.groups()
            self._parse_simple_trainer(trainer, team)
        # Matches: Empty line
        elif line == "":
            self.parse_default(line)

            if self._current_team:
                current_trainer = self._trainers[self._category][self._current_trainer]
                teams = len(current_trainer)

                if teams > 0 and "Default" in current_trainer:
                    self._trainers[self._category][self._current_trainer]["Team 1"] = (
                        current_trainer["Default"]
                    )
                    del current_trainer["Default"]

                extension = f"Team {teams + 1}" if teams > 0 else "Default"
                current_trainer[extension] = self._current_team
                self._current_team = []

            if self._current_trainer in self._trainers:
                del self._trainers[self._current_trainer]
        # Matches: Next line matches ^ (Lv. XX)
        elif "Lv." in next_line:
            self._set_category(line)
        # Default: regular text line
        else:
            self.parse_default(line)

    def _parse_simple_trainer(self, trainer: str, team: str) -> None:
        # Extract trainer name and extension if present
        if match := re.match(r"^(.+?) \((.)\)$", trainer):
            trainer, extension = match.groups()
            extension = f"({extension})"
        elif teams := len(self._trainers[self._category].get(trainer, {})):
            extension = f"Team {teams + 1}"
            if "Default" in self._trainers[self._category][trainer]:
                self._trainers[self._category][trainer][f"Team 1"] = self._trainers[
                    self._category
                ][trainer]["Default"]
                del self._trainers[self._category][trainer]["Default"]
        else:
            extension = "Default"

        # Setup trainer entry if it doesn't exist
        if not trainer in self._trainers[self._category]:
            self._trainers[self._category][trainer] = {}

        # Parse team Pokémon
        pokemon = []
        levels = []
        for slot in team.split(", "):
            if match := re.match(r"^(.+?) Lv. (\d+)$", slot):
                name, level = match.groups()
                pokemon.append(name)
                levels.append(f"Lv. {level}")
            else:
                self.logger.warning(f"Could not parse team slot: {slot}")

        # Add team to trainer entry
        self._trainers[self._category][trainer][extension] = [
            format_pokemon_card_grid(pokemon, extra_info=levels)
        ]

    def _format_trainers(self) -> str:
        md = ""

        # Loop through categories
        for category, trainers in self._trainers.items():
            md += f"#### {category}\n\n"

            # Loop through trainers
            for trainer, teams in trainers.items():
                md += f"**{trainer}**\n\n"

                # Loop through teams
                if len(teams) == 1 and "Default" in teams:
                    md += "\n".join(teams["Default"]) + "\n\n"
                else:
                    for extension, team_md in teams.items():
                        md += f'=== "{extension}"\n\n'
                        md += (
                            "\n".join(
                                f"\t{line}".rstrip()
                                for line in "\n".join(team_md).splitlines()
                            )
                            + "\n\n"
                        )

        return md
