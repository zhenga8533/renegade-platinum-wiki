"""
Parser for Wild Pokémon documentation file.

This parser:
1. Reads data/documentation/Wild Pokemon.txt
2. Generates a markdown file to docs/reference/wild_pokemon.md
3. Generates JSON data files to data/locations/ for each location with wild encounter information
"""

import re
from typing import Any, Dict

from rom_wiki_core.parsers.location_parser import LocationParser
from rom_wiki_core.utils.core.loader import PokeDBLoader
from rom_wiki_core.utils.formatters.markdown_formatter import (
    format_pokemon,
    format_type_badge,
)


class WildPokemonParser(LocationParser):
    """Parser for Wild Pokémon documentation.

    Args:
        LocationParser (_type_): Location parser base class.
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

        # Register tracking key for wild encounters
        self._register_tracking_key("wild_encounters")

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
            # Initialize location data for JSON generation
            location_raw = line

            # Check if this is a sublocation (contains ~)
            if " ~ " in location_raw:
                # Parse the parent and sublocation
                parent_location, sublocation_name = self._parse_location_name(
                    location_raw
                )

                # If we're switching to a new parent location, initialize it
                if parent_location != self._current_location:
                    self._current_location = parent_location
                    self._initialize_location_data(parent_location)

                # Set the sublocation
                self._current_sublocation = sublocation_name or location_raw
                self._ensure_sublocation_exists(
                    self._current_location, self._current_sublocation
                )

                # Clear wild encounters for this sublocation on first encounter
                sublocation_key = (
                    f"{self._current_location}/{self._current_sublocation}"
                )
                self._clear_location_data_on_first_encounter(
                    "wild_encounters", "wild_encounters", sublocation_key
                )

                # Use #### for sublocation header
                self._markdown += f"#### {line}\n\n"
            else:
                # This is a main location
                parent_location, sublocation_name = self._parse_location_name(
                    location_raw
                )
                self._current_location = parent_location
                self._current_sublocation = sublocation_name or ""
                self._initialize_location_data(location_raw)

                self._markdown += f"### {line}\n\n"

            self._levels = {}  # Reset levels for new location/sublocation
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
        """Format wild Pokémon data into markdown and save to JSON.

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

        # Prepare JSON data
        encounter_list = []

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

            # Add to JSON data
            encounter_list.append(
                {
                    "pokemon": name,
                    "chance": int(chance),
                    "level": level_range,  # Changed from level_range to level to match generator expectations
                    "types": types,
                }
            )

        # Save encounters to location data
        if has_encounters:
            self._add_wild_encounters_to_location(method, encounter_list, level_range)

        return md + "\n" if has_encounters else ""

    def _add_wild_encounters_to_location(
        self, method: str, encounters: list[Dict[str, Any]], level_range: str
    ) -> None:
        """Add wild encounter data to the current location or sublocation.

        Args:
            method (str): The encounter method (e.g., "Morning", "Surf", "Old Rod").
            encounters (list[Dict[str, Any]]): List of encounter data.
            level_range (str): The level range for encounters (not used, kept for compatibility).
        """
        if not self._current_location:
            return

        if self._current_location not in self._locations_data:
            self._initialize_location_data(self._current_location)

        # Get or create target location/sublocation
        if self._current_sublocation:
            target = self._get_or_create_sublocation(
                self._locations_data[self._current_location], self._current_sublocation
            )
        else:
            target = self._locations_data[self._current_location]

        # Initialize wild_encounters dict if needed
        if "wild_encounters" not in target:
            target["wild_encounters"] = {}

        # Add encounters for this method - store as list directly to match generator expectations
        target["wild_encounters"][method] = encounters

    def _initialize_location_data(self, location_raw: str) -> None:
        """Initialize data structure for a location.

        Args:
            location_raw (str): The raw location name (may include sublocation).
        """
        # Call parent class initialization
        super()._initialize_location_data(location_raw)

        # Use centralized method to clear wild encounters on first encounter
        self._clear_location_data_on_first_encounter(
            "wild_encounters", "wild_encounters"
        )
