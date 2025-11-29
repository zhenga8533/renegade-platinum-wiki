"""
Parser for Trainer Pokémon documentation file.

This parser:
1. Reads data/documentation/Trainer Pokemon.txt
2. Generates a markdown file to docs/reference/trainer_pokemon.md
3. Generates JSON data files to data/locations/ for each location with trainer information
"""

import re
from typing import Any, Dict, Optional

from src.utils.core.loader import PokeDBLoader
from src.utils.formatters.markdown_formatter import (
    format_ability,
    format_item,
    format_move,
    format_pokemon,
    format_type_badge,
)

from .location_parser import LocationParser


class TrainerPokemonParser(LocationParser):
    """Parser for Trainer Pokémon documentation.

    Args:
        LocationParser (_type_): Location parser base class.
    """

    def __init__(self, input_file: str, output_dir: str = "docs/reference"):
        """Initialize the Trainer Pokémon parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/reference".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Changes", "Area Changes"]

        # Starter Pokémon - always ordered as Turtwig, Chimchar, Piplup
        self._starter_trainers = [
            "PKMN Trainer Barry",
            "PKMN Trainer Dawn",
            "PKMN Trainer Lucas",
        ]
        self._starter_order = ["Turtwig", "Chimchar", "Piplup"]

        # Area Changes States
        self._category = None
        self._current_trainer = None
        self._current_team_pokemon = []  # Raw Pokemon data for current detailed team

        # Structure: {'Normal Trainers': {'Name': {'Default': {'type': 'simple'/'detailed', 'pokemon': [...]}}}}
        self._trainers = {}

        # Register tracking key for trainers
        self._register_tracking_key("trainers")

    def _set_category(self, category: str) -> None:
        """Set the current category for trainers.

        Args:
            category (str): The category to set.
        """
        if category not in self._trainers:
            self._trainers[category] = {}
        self._category = category

    def _get_trainer_extension(self, trainer_name: str, existing_teams_count: int) -> str:
        """Get the extension name for a trainer team variation.

        Args:
            trainer_name (str): The trainer's name.
            existing_teams_count (int): Number of teams already recorded for this trainer.

        Returns:
            str: The extension name (e.g., "Turtwig", "Trainer 2", "Default").
        """
        if trainer_name in self._starter_trainers:
            # For starter trainers, use hardcoded order: Turtwig, Chimchar, Piplup
            if existing_teams_count < len(self._starter_order):
                return self._starter_order[existing_teams_count]
            return "Default"
        elif existing_teams_count > 0:
            return f"Trainer {existing_teams_count + 1}"
        else:
            return "Default"

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

            # Initialize location data for JSON generation
            location_raw = line
            parent_location, sublocation_name = self._parse_location_name(location_raw)
            self._current_location = parent_location
            self._current_sublocation = sublocation_name or ""
            self._initialize_location_data(location_raw)

            self._markdown += f"### {line}\n\n"
            self._set_category("Normal Trainers")
        elif line == "---":
            pass
        # Matches: sub-headings (nested sublocations from ~)
        elif next_line.startswith("~"):
            self._markdown += self._format_trainers()
            self._trainers = {}

            nested_sublocation = line
            # Parse location name for potential " - " pattern
            parent_location, base_sublocation = self._parse_location_name(
                nested_sublocation
            )

            # Update current location context
            if parent_location != self._current_location:
                # This is a new parent location
                self._current_location = parent_location
                self._current_sublocation = base_sublocation or ""
                self._initialize_location_data(nested_sublocation)
            else:
                # This is a sublocation under the current location
                self._current_sublocation = nested_sublocation
                self._ensure_sublocation_exists(
                    self._current_location, nested_sublocation
                )

            # Clear trainers on first encounter for this sublocation
            sublocation_key = (
                f"{self._current_location}/{self._current_sublocation}"
                if self._current_sublocation
                else self._current_location
            )
            self._clear_location_data_on_first_encounter(
                "trainers", "trainers", sublocation_key
            )

            self._markdown += f"#### {line}\n\n"
            self._set_category("Normal Trainers")
        elif line.startswith("~"):
            pass
        # Matches: Pokémon (Lv. XX) @ Item / Nature / Ability / Move1, Move2, Move3, Move4
        elif match := re.match(
            r"^(.+?) \(Lv. (\d+)\) @ (.+?)/(.+?)/(.+?)/(.+?)$", line
        ):
            pokemon, level, item, nature, ability, moves = match.groups()
            item = item.strip()
            nature = nature.strip()
            ability = ability.strip()
            moves_list = [m.strip() for m in moves.strip().split(", ")]

            # Store raw Pokemon data
            self._current_team_pokemon.append(
                {
                    "pokemon": pokemon,
                    "level": int(level),
                    "item": item,
                    "nature": nature,
                    "ability": ability,
                    "moves": moves_list,
                }
            )

            # Add to JSON data
            if self._current_trainer:
                self._add_detailed_trainer_to_location(
                    self._current_trainer,
                    pokemon,
                    ability,
                    level,
                    item,
                    ", ".join(moves_list),
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

            # Save detailed team if we have one
            if self._current_team_pokemon and self._current_trainer:
                current_trainer = self._trainers[self._category][self._current_trainer]

                # Determine extension for starter trainers or regular trainers
                extension = self._get_trainer_extension(
                    self._current_trainer, len(current_trainer)
                )

                current_trainer[extension] = {
                    "type": "detailed",
                    "pokemon": self._current_team_pokemon,
                }
                self._current_team_pokemon = []

            if self._current_trainer in self._trainers:
                del self._trainers[self._current_trainer]
        # Matches: Next line matches ^ (Lv. XX)
        elif "Lv." in next_line:
            self._set_category(line)
        # Default: regular text line
        else:
            self.parse_default(line)

    def _parse_simple_trainer(self, trainer: str, team: str) -> None:
        """Parse a simple trainer (just Pokemon name and level).

        Args:
            trainer (str): Trainer name, possibly with variation marker like (!)
            team (str): Comma-separated list of "Pokemon Lv. XX"
        """
        # Parse team Pokémon first to determine extension for starter trainers
        pokemon_list = []
        for slot in team.split(", "):
            if match := re.match(r"^(.+?) Lv. (\d+)$", slot):
                name, level = match.groups()
                poke_data = PokeDBLoader.load_pokemon(name)
                if poke_data is None:
                    self.logger.warning(f"Could not load data for Pokémon: {name}")
                    continue

                types = poke_data.types if poke_data else []
                pokemon_list.append(
                    {
                        "pokemon": name,
                        "level": int(level),
                        "types": types,
                        "poke_data": poke_data,  # Keep for markdown formatting
                    }
                )
            else:
                self.logger.warning(f"Could not parse team slot: {slot}")

        # Extract trainer name and extension if present
        if match := re.match(r"^(.+?) \((.)\)$", trainer):
            trainer, extension = match.groups()
            extension = f"({extension})"
        else:
            teams = len(self._trainers[self._category].get(trainer, {}))
            extension = self._get_trainer_extension(trainer, teams)

        # Setup trainer entry if it doesn't exist
        if trainer not in self._trainers[self._category]:
            self._trainers[self._category][trainer] = {}

        # Store raw data
        self._trainers[self._category][trainer][extension] = {
            "type": "simple",
            "pokemon": pokemon_list,
        }

        # Add simple trainer to location JSON data
        json_pokemon = [
            {"pokemon": p["pokemon"], "level": p["level"], "types": p["types"]}
            for p in pokemon_list
        ]
        self._add_simple_trainer_to_location(trainer, json_pokemon, extension)

    def _format_trainers(self) -> str:
        """Format trainer data into markdown.

        Returns:
            str: Formatted markdown string
        """
        md = ""

        # Loop through categories
        for category, trainers in self._trainers.items():
            md += f"#### {category}\n\n"

            # Loop through trainers
            for trainer, teams in trainers.items():
                md += f"**{trainer}**\n\n"

                # Loop through teams
                if len(teams) == 1 and "Default" in teams:
                    md += self._format_team(teams["Default"]) + "\n\n"
                else:
                    for extension, team_data in teams.items():
                        # Rename "Default" to "Trainer 1" when there are multiple teams
                        display_name = (
                            "Trainer 1" if extension == "Default" else extension
                        )
                        md += f'=== "{display_name}"\n\n'
                        formatted = self._format_team(team_data)
                        # Indent each line
                        md += (
                            "\n".join(
                                f"\t{line}".rstrip() for line in formatted.splitlines()
                            )
                            + "\n\n"
                        )

        return md

    def _format_team(self, team_data: Dict[str, Any]) -> str:
        """Format a single team into markdown.

        Args:
            team_data (Dict[str, Any]): Team data with 'type' and 'pokemon' keys

        Returns:
            str: Formatted markdown table
        """
        team_type = team_data["type"]
        pokemon_list = team_data["pokemon"]

        if team_type == "simple":
            # Simple format: | Pokémon | Level | Type(s) |
            lines = [
                "| Pokémon | Level | Type(s) |",
                "|:-------:|:------|:-------|",
            ]
            for p in pokemon_list:
                type_badges = " ".join([format_type_badge(t) for t in p["types"]])
                type_html = f"<div class='badges-vstack'>{type_badges}</div>"
                lines.append(
                    f"| {format_pokemon(p['poke_data'])} | Lv. {p['level']} | {type_html} |"
                )
            return "\n".join(lines)

        else:  # detailed
            # Detailed format: | Pokémon | Attributes | Moves |
            lines = [
                "| Pokémon | Attributes | Moves |",
                "|:-------:|:-----------|:------|",
            ]
            for p in pokemon_list:
                pokemon_md = format_pokemon(p["pokemon"])
                item_md = format_item(p["item"])
                moves_md = "<br>".join([format_move(move) for move in p["moves"]])
                ability_md = format_ability(p["ability"])

                lines.append(
                    f"| {pokemon_md} | **Level:** Lv. {p['level']}<br>**Item:**{item_md}<br>**Nature:** {p['nature']}<br>**Ability:** {ability_md}| {moves_md} |"
                )
            return "\n".join(lines)

    def _add_simple_trainer_to_location(
        self, trainer_name: str, team: list[Dict[str, Any]], extension: str = "Default"
    ) -> None:
        """Add a simple trainer (no detailed moves/items) to location data.

        Args:
            trainer_name (str): The trainer's name.
            team (list[Dict[str, Any]]): List of Pokemon data for the team.
            extension (str): Team variation identifier.
        """
        if not self._current_location:
            return

        if self._current_location not in self._locations_data:
            self._initialize_location_data(self._current_location)

        trainer_data = {
            "name": trainer_name,
            "category": self._category or "Normal Trainers",
            "team": team,
            "sublocation": self._current_sublocation,
        }

        if extension != "Default":
            trainer_data["team_variation"] = extension

        # Add to sublocation if specified
        if self._current_sublocation:
            target = self._get_or_create_sublocation(
                self._locations_data[self._current_location], self._current_sublocation
            )
            if "trainers" not in target:
                target["trainers"] = []
            target["trainers"].append(trainer_data)
        else:
            if "trainers" not in self._locations_data[self._current_location]:
                self._locations_data[self._current_location]["trainers"] = []
            self._locations_data[self._current_location]["trainers"].append(
                trainer_data
            )

    def _should_skip_detailed_trainer(self, existing_trainers: list[Dict[str, Any]]) -> bool:
        """Check if detailed trainer data should be skipped.

        Detailed breakdown in documentation is just reference info, not replacement teams.
        This handles cases like Dawn/Lucas where simple teams are the actual teams.

        Args:
            existing_trainers (list[Dict[str, Any]]): List of existing trainer entries.

        Returns:
            bool: True if detailed trainer should be skipped, False otherwise.
        """
        if not existing_trainers:
            return False

        # If we found existing simple teams (team variations), don't add detailed version
        for trainer in existing_trainers:
            if not trainer.get("team"):
                continue
            # Check if first Pokemon has ability (indicates detailed team)
            if "ability" in trainer["team"][0]:
                return False

        return True

    def _get_target_location(self) -> Optional[Dict[str, Any]]:
        """Get the target location or sublocation for adding trainer data.

        Returns:
            Optional[Dict[str, Any]]: The target location dictionary, or None if invalid.
        """
        if self._current_sublocation:
            return self._get_or_create_sublocation(
                self._locations_data[self._current_location], self._current_sublocation
            )
        return self._locations_data[self._current_location]

    def _find_existing_trainers(
        self, target: Dict[str, Any], trainer_name: str
    ) -> list[Dict[str, Any]]:
        """Find existing trainer entries in the target location.

        Args:
            target (Dict[str, Any]): Target location data.
            trainer_name (str): The trainer's name.

        Returns:
            list[Dict[str, Any]]: List of existing trainer entries.
        """
        if "trainers" not in target:
            target["trainers"] = []

        return [
            t
            for t in target["trainers"]
            if t["name"] == trainer_name
            and t.get("sublocation") == self._current_sublocation
        ]

    def _prepare_trainer_data(
        self, existing_trainers: list[Dict[str, Any]], target: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get or create trainer data entry for detailed Pokemon.

        Args:
            existing_trainers (list[Dict[str, Any]]): List of existing trainer entries.
            target (Dict[str, Any]): Target location data.

        Returns:
            Dict[str, Any]: The trainer data dictionary.
        """
        if existing_trainers:
            trainer_data = existing_trainers[0]
            trainer_data["category"] = "Important Trainers"
            # Clear team on first detailed Pokemon (will be repopulated)
            if not trainer_data["team"] or "ability" not in trainer_data["team"][0]:
                trainer_data["team"] = []
            return trainer_data

        # Create new trainer entry
        trainer_data = {
            "name": self._current_trainer,
            "category": "Important Trainers",
            "team": [],
            "sublocation": self._current_sublocation,
        }
        target["trainers"].append(trainer_data)
        return trainer_data

    def _add_detailed_trainer_to_location(
        self,
        trainer_name: str,
        pokemon: str,
        ability: str,
        level: str,
        item: Optional[str],
        moves: str,
    ) -> None:
        """Add or update a detailed trainer (with moves/items) to location data.

        Args:
            trainer_name (str): The trainer's name.
            pokemon (str): Pokemon name.
            ability (str): Pokemon ability.
            level (str): Pokemon level.
            item (Optional[str]): Pokemon held item.
            moves (str): Pokemon moves (comma-separated).
        """
        if not self._current_location:
            return

        if self._current_location not in self._locations_data:
            self._initialize_location_data(self._current_location)

        # Get target location/sublocation
        target = self._get_target_location()
        if not target:
            return

        # Find existing trainer entries
        existing_trainers = self._find_existing_trainers(target, trainer_name)

        # Skip if simple team variations already exist
        if self._should_skip_detailed_trainer(existing_trainers):
            return

        # Get or create trainer data entry
        trainer_data = self._prepare_trainer_data(existing_trainers, target)

        # Add Pokemon to team
        poke_data = PokeDBLoader.load_pokemon(pokemon)
        types = poke_data.types if poke_data else []

        pokemon_entry = {
            "pokemon": pokemon,
            "ability": ability,
            "level": int(level),
            "moves": [move.strip() for move in moves.split(", ")],
            "types": types,
        }

        if item:
            pokemon_entry["item"] = item

        trainer_data["team"].append(pokemon_entry)

    def _initialize_location_data(self, location_raw: str) -> None:
        """Initialize data structure for a location.

        Args:
            location_raw (str): The raw location name (may include sublocation).
        """
        # Call parent class initialization
        super()._initialize_location_data(location_raw)

        # Use centralized method to clear trainers on first encounter
        self._clear_location_data_on_first_encounter("trainers", "trainers")
