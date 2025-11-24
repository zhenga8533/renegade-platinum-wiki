"""
Parser for Evolution Changes documentation file.

This parser:
1. Reads data/documentation/Evolution Changes.txt
2. Updates pokemon evolution data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/evolution_changes.md
"""

import re

from src.utils.core.loader import PokeDBLoader
from src.utils.data.models import EvolutionDetails
from src.utils.formatters.markdown_formatter import format_item, format_pokemon
from src.utils.formatters.table_formatter import create_table_header
from src.utils.services.evolution_service import EvolutionService
from src.utils.text.text_util import name_to_id

from .base_parser import BaseParser


class EvolutionChangesParser(BaseParser):
    """Parser for Evolution Changes documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/changes"):
        """Initialize the Evolution Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/changes".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["Item Interaction Changes", "Level Changes", "Method Changes"]

        # Table State
        self._is_table_open = False

    def handle_section_change(self, new_section: str) -> None:
        """Handle logic when changing sections.

        Args:
            new_section (str): Name of the new section being entered
        """
        self._is_table_open = False
        super().handle_section_change(new_section)

    def _start_table(self, headers: list[str]) -> None:
        """Start a markdown table with the given headers.

        Args:
            headers (list[str]): Column headers for the table
        """
        if not self._is_table_open:
            self._markdown += (
                create_table_header(headers, ["center", "center", "left"]) + "\n"
            ) + "\n"
            self._is_table_open = True

    def _update_evolution(
        self,
        pokemon: str,
        evolution: str,
        evolution_details: EvolutionDetails,
        keep_existing: bool,
        log_message: str,
    ) -> tuple[str, str]:
        """Update evolution chain data for a Pokemon.

        Args:
            pokemon (str): Pokemon name
            evolution (str): Evolution target name
            evolution_details (EvolutionDetails): Evolution details to apply
            keep_existing (bool): Whether to keep existing evolution methods
            log_message (str): Log message for successful update

        Returns:
            tuple[str, str]: Formatted Pokemon and evolution names for markdown
        """
        pokemon_id = name_to_id(pokemon)
        evolution_id = name_to_id(evolution)

        # Load the Pokemon's evolution chain
        pokemon_data = PokeDBLoader.load_pokemon(pokemon_id)
        if pokemon_data and pokemon_data.evolution_chain:
            # Update the evolution chain
            EvolutionService.update_evolution_chain(
                pokemon_id=pokemon_id,
                evolution_id=evolution_id,
                evolution_chain=pokemon_data.evolution_chain,
                evolution_details=evolution_details,
                keep_existing=keep_existing,
            )

            self.logger.info(log_message.format(pokemon=pokemon, evolution=evolution))

        # Return formatted names for markdown
        return format_pokemon(pokemon_id), format_pokemon(evolution_id)

    def parse_item_interaction_changes(self, line: str) -> None:
        """Parse a line from the Item Interaction Changes section.

        Args:
            line (str): A line from the Item Interaction Changes section.
        """
        # Matches: - Pokemon: Now able to evolve into Evolution by using an Item.
        if match := re.match(
            r"^- (.+?): Now able to evolve into (.+?) by using an? (.+?)\.$", line
        ):
            pokemon, evolution, item = match.groups()
            item_id = name_to_id(item)

            # Create evolution details and update
            evolution_details = EvolutionDetails(trigger="use-item", item=item_id)
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=True,
                log_message="Updated {pokemon} -> {evolution} evolution via " + item,
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "Item"])
            item_formatted = format_item(item_id)
            self._markdown += (
                f"| {pokemon_fmt} | {evolution_fmt} | {item_formatted} |\n"
            )
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_level_changes(self, line: str) -> None:
        """Parse a line from the Level Changes section.

        Args:
            line (str): A line from the Level Changes section.
        """
        # Matches: - Pokemon: Now evolves into Evolution at Level X.
        if match := re.match(
            r"^- (.+?): Now evolves into (.+?) at Level (\d+)\.$", line
        ):
            pokemon, evolution, level = match.groups()
            level_int = int(level)

            # Create evolution details and update
            evolution_details = EvolutionDetails(
                trigger="level-up", min_level=level_int
            )
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=False,
                log_message=f"Updated {{pokemon}} -> {{evolution}} evolution to level {level}",
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "Level"])
            self._markdown += f"| {pokemon_fmt} | {evolution_fmt} | Level {level} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_method_changes(self, line: str) -> None:
        """Parse a line from the Method Changes section.

        Args:
            line (str): A line from the Method Changes section.
        """
        # Matches: - Pokemon: Now able to evolve into Evolution at Level X.
        if match := re.match(
            r"^- (.+?): Now able to evolve into (.+?) at Level (\d+)\.$", line
        ):
            pokemon, evolution, level = match.groups()
            level_int = int(level)

            # Create evolution details and update
            evolution_details = EvolutionDetails(
                trigger="level-up", min_level=level_int
            )
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=False,
                log_message=f"Added {{pokemon}} -> {{evolution}} evolution method via level {level}",
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "New Method"])
            self._markdown += f"| {pokemon_fmt} | {evolution_fmt} | Level {level} |\n"

        # Matches: - Pokemon: Now only able to evolve into Evolution with the Item.
        # Or: - Pokemon: Now only evolves into Evolution with the Item.
        elif match := re.match(
            r"^- (.+?): Now only (?:able to )?evolves? into (.+?) with the (.+?)\.$",
            line,
        ):
            pokemon, evolution, item = match.groups()
            item_id = name_to_id(item)

            # Create evolution details and update
            evolution_details = EvolutionDetails(trigger="use-item", item=item_id)
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=False,
                log_message=f"Replaced {{pokemon}} -> {{evolution}} evolution with {item} only",
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "New Method"])
            item_formatted = format_item(item_id)
            self._markdown += (
                f"| {pokemon_fmt} | {evolution_fmt} | {item_formatted} |\n"
            )

        # Matches: - Pokemon: Now able to evolve into Evolution by using an Item.
        elif match := re.match(
            r"^- (.+?): Now able to evolve into (.+?) by using an? (.+?)\.$", line
        ):
            pokemon, evolution, item = match.groups()
            item_id = name_to_id(item)

            # Create evolution details and update
            evolution_details = EvolutionDetails(trigger="use-item", item=item_id)
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=True,
                log_message=f"Added {{pokemon}} -> {{evolution}} evolution method via {item}",
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "New Method"])
            item_formatted = format_item(item_id)
            self._markdown += (
                f"| {pokemon_fmt} | {evolution_fmt} | {item_formatted} |\n"
            )

        # Matches: - Pokemon: Now evolves into Evolution when happy regardless of the time.
        elif match := re.match(
            r"^- (.+?): Now evolves into (.+?) when happy regardless of the time\.$",
            line,
        ):
            pokemon, evolution = match.groups()

            # Create evolution details and update (happiness with no time restriction)
            evolution_details = EvolutionDetails(
                trigger="level-up",
                min_happiness=160,
                time_of_day="",  # Empty string means any time
            )
            pokemon_fmt, evolution_fmt = self._update_evolution(
                pokemon,
                evolution,
                evolution_details,
                keep_existing=False,
                log_message="Updated {pokemon} -> {evolution} to evolve when happy (any time)",
            )

            # Start table and add row
            self._start_table(["Pokemon", "Evolution", "New Method"])
            self._markdown += (
                f"| {pokemon_fmt} | {evolution_fmt} | Happiness (any time of day) |\n"
            )

        # Default: regular text line
        else:
            self.parse_default(line)
