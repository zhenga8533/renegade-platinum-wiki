"""
Parser for Move Changes documentation file.

This parser:
1. Reads data/documentation/Move Changes.txt
2. Updates pokemon Move data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/move_changes.md
"""

import re

import orjson

from src.utils.core.loader import PokeDBLoader
from src.utils.data.models import Move
from src.utils.formatters.markdown_formatter import format_move
from src.utils.services.move_service import MoveService

from .base_parser import BaseParser


class MoveChangesParser(BaseParser):
    """Parser for  documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/changes"):
        """Initialize the Move Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/changes".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["General Changes", "Move Replacements", "Move Modifications"]

        # Move Modification States
        self._is_table_open = False
        self._current_move = ""
        self._is_move_open = False

    def _update_all_moves_to_gen7(self) -> None:
        """Update all existing moves in parsed data to match gen7 stats.

        This method:
        1. Loads all moves from gen7 source data
        2. For each move that exists in parsed data, updates its stats to match gen7
        3. Skips moves that don't exist in parsed data (they'll be copied separately)
        """
        # Get paths to gen7 and parsed move directories
        data_dir = PokeDBLoader.get_data_dir()
        gen7_move_dir = data_dir.parent / "gen7" / "move"
        parsed_move_dir = PokeDBLoader.get_category_path("move")

        if not gen7_move_dir.exists():
            self.logger.warning(f"Gen7 move directory not found: {gen7_move_dir}")
            return

        # Iterate through all gen7 moves
        for gen7_move_path in gen7_move_dir.glob("*.json"):
            move_id = gen7_move_path.stem
            parsed_move_path = parsed_move_dir / f"{move_id}.json"

            # Only update if the move already exists in parsed data
            if parsed_move_path.exists():
                # Load gen7 move from JSON directly
                try:
                    with open(gen7_move_path, "rb") as f:
                        gen7_data = orjson.loads(f.read())
                    gen7_move = Move(**gen7_data)
                except (OSError, IOError, ValueError) as e:
                    self.logger.warning(f"Error loading gen7 move '{move_id}': {e}")
                    continue

                # Load parsed move using PokeDBLoader
                parsed_move = PokeDBLoader.load_move(move_id)
                if not parsed_move:
                    continue

                # Update stats to match gen7
                updated = False

                # Update power
                if hasattr(gen7_move, "power") and hasattr(parsed_move, "power"):
                    gen7_power = self._get_version_value(gen7_move.power)
                    parsed_power = self._get_version_value(parsed_move.power)
                    if gen7_power != parsed_power:
                        self._set_all_versions(parsed_move.power, gen7_power)
                        updated = True

                # Update accuracy
                if hasattr(gen7_move, "accuracy") and hasattr(parsed_move, "accuracy"):
                    gen7_acc = self._get_version_value(gen7_move.accuracy)
                    parsed_acc = self._get_version_value(parsed_move.accuracy)
                    if gen7_acc != parsed_acc:
                        self._set_all_versions(parsed_move.accuracy, gen7_acc)
                        updated = True

                # Update PP
                if hasattr(gen7_move, "pp") and hasattr(parsed_move, "pp"):
                    gen7_pp = self._get_version_value(gen7_move.pp)
                    parsed_pp = self._get_version_value(parsed_move.pp)
                    if gen7_pp != parsed_pp:
                        self._set_all_versions(parsed_move.pp, gen7_pp)
                        updated = True

                # Update effect_chance
                if hasattr(gen7_move, "effect_chance") and hasattr(
                    parsed_move, "effect_chance"
                ):
                    gen7_chance = self._get_version_value(gen7_move.effect_chance)
                    parsed_chance = self._get_version_value(parsed_move.effect_chance)
                    if gen7_chance != parsed_chance:
                        self._set_all_versions(parsed_move.effect_chance, gen7_chance)
                        updated = True

                # Update priority
                if hasattr(gen7_move, "priority") and hasattr(parsed_move, "priority"):
                    if gen7_move.priority != parsed_move.priority:
                        parsed_move.priority = gen7_move.priority
                        updated = True

                # Update type
                if hasattr(gen7_move, "type") and hasattr(parsed_move, "type"):
                    gen7_type = self._get_version_value(gen7_move.type)
                    parsed_type = self._get_version_value(parsed_move.type)
                    if gen7_type != parsed_type:
                        self._set_all_versions(parsed_move.type, gen7_type)
                        updated = True

                # Save if updated
                if updated:
                    PokeDBLoader.save_move(move_id, parsed_move)
                    self.logger.info(f"Updated move '{move_id}' to gen7 stats")

    def _get_version_value(self, field):
        """Get a value from a field, handling both version groups and plain values."""
        if hasattr(field, "__slots__"):
            # Version group object - get first version's value
            for version_key in field.__slots__:
                return getattr(field, version_key, None)
        return field

    def _set_all_versions(self, field, value):
        """Set a value for all version groups in a field."""
        if hasattr(field, "__slots__"):
            # Version group object - set all versions
            for version_key in field.__slots__:
                setattr(field, version_key, value)
        # If not a version group object, can't set it here (handled by caller)

    def handle_section_change(self, new_section: str) -> None:
        """Handle logic when changing sections.

        Args:
            new_section (str): The new section being entered.
        """

        if new_section == "General Changes":
            self._update_all_moves_to_gen7()

        super().handle_section_change(new_section)

    def parse_general_changes(self, line: str) -> None:
        """Parse a line from the General Changes section.

        Args:
            line (str): A line from the General Changes section.
        """
        self.parse_default(line)

    def parse_move_replacements(self, line: str) -> None:
        """Parse a line from the Move Replacements section.

        Args:
            line (str): A line from the Move Replacements section.
        """
        if line == "Old Move                New Move":
            self._markdown += "| Old Move | New Move |\n"
        elif line == "---------               ---------":
            self._markdown += "|:---------|:---------|\n"
        # Matches: Old Move  New Move
        elif match := re.match(r"^(.+?)\s{2,}(.+)$", line):
            old_move, new_move = match.groups()

            # Copy the new move from gen7 if it doesn't exist
            MoveService.copy_new_move(new_move)

            self._markdown += f"| {format_move(old_move)} | {format_move(new_move)} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_move_modifications(self, line: str) -> None:
        """Parse a line from the Move Modifications section.

        Args:
            line (str): A line from the Move Modifications section.
        """
        next_line = self.peek_line(1) or ""

        if match := re.match(r"^(.+?): (.+?) >> (.+?)$", line):
            key, old_value, new_value = match.groups()

            # Update the move attribute using MoveService
            MoveService.update_move_attribute(self._current_move, key, new_value)

            if self._is_move_open:
                move_md = "└──"
            else:
                move_md = format_move(self._current_move)
                self._is_move_open = True

            self._markdown += f"| {move_md} | {key} | {old_value} | {new_value} |\n"
        elif ">>" in next_line:
            self._current_move = line
            self._is_move_open = False
            if not self._is_table_open:
                self._markdown += (
                    "| Move | Attribute | Old | New |\n"
                    "|:-----|:----------|:----|:----|\n"
                )
                self._is_table_open = True
        elif line or not self._is_table_open:
            self.parse_default(line)
