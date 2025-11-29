"""
Parser for Pokemon Changes documentation file.

This parser:
1. Reads data/documentation/Pokemon Changes.txt
2. Updates pokemon data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/pokemon_changes.md
"""

import re

import orjson

from src.utils.core.config import VERSION_GROUP
from src.utils.core.loader import PokeDBLoader
from src.utils.data.models import Pokemon
from src.utils.formatters.markdown_formatter import (
    format_ability,
    format_checkbox,
    format_item,
    format_move,
    format_pokemon,
    format_pokemon_card_grid,
    format_type_badge,
)
from src.utils.services.attribute_service import AttributeService
from src.utils.services.pokemon_item_service import PokemonItemService
from src.utils.text.text_util import name_to_id

from .base_parser import BaseParser


class PokemonChangesParser(BaseParser):
    """Parser for Pokemon Changes documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/changes"):
        """Initialize the Pokemon Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/changes".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = [
            "General Changes",
            "Held Item Exceptions",
            "Other Changes",
            "Custom Changes",
            "Specific Changes",
        ]

        # Specific Changes States
        self._current_pokemon = ""
        self._current_attribute = ""
        self._is_table_open = False
        self._temporary_markdown = ""

        # Track Pokemon with held items updated to skip later
        self._held_item_updated = set()

    def _update_all_pokemon_to_gen7(self) -> None:
        """Update all existing Pokemon in parsed data to match gen7 stats.

        This method:
        1. Loads all Pokemon from gen7 source data
        2. For each Pokemon that exists in parsed data, updates base stats, types, and held items to match gen7
        3. Sets egg cycle to 0 for all Pokemon
        """
        # Get paths to gen7 and parsed Pokemon directories
        data_dir = PokeDBLoader.get_data_dir()
        gen7_pokemon_dir = data_dir.parent / "gen7" / "pokemon" / "default"
        parsed_pokemon_dir = PokeDBLoader.get_category_path("pokemon") / "default"

        if not gen7_pokemon_dir.exists():
            self.logger.warning(f"Gen7 Pokemon directory not found: {gen7_pokemon_dir}")
            return

        # Iterate through all gen7 Pokemon
        for gen7_pokemon_path in gen7_pokemon_dir.glob("*.json"):
            pokemon_id = gen7_pokemon_path.stem
            parsed_pokemon_path = parsed_pokemon_dir / f"{pokemon_id}.json"

            # Only update if the Pokemon already exists in parsed data
            if parsed_pokemon_path.exists():
                # Load gen7 Pokemon from JSON
                try:
                    with open(gen7_pokemon_path, "rb") as f:
                        gen7_data = orjson.loads(f.read())
                    gen7_pokemon = Pokemon(**gen7_data)
                except (OSError, IOError, ValueError) as e:
                    self.logger.warning(
                        f"Error loading gen7 Pokemon '{pokemon_id}': {e}"
                    )
                    continue

                # Load parsed Pokemon using PokeDBLoader
                parsed_pokemon = PokeDBLoader.load_pokemon(
                    pokemon_id, subfolder="default"
                )
                if not parsed_pokemon:
                    continue

                updated = False

                # Update base stats
                if gen7_pokemon.stats != parsed_pokemon.stats:
                    parsed_pokemon.stats = gen7_pokemon.stats
                    updated = True

                # Update types
                if gen7_pokemon.types != parsed_pokemon.types:
                    parsed_pokemon.types = gen7_pokemon.types
                    updated = True

                # Update held items (only if item exists in gen4 parsed data)
                gen7_held_items = {}
                for item_id, versions in gen7_pokemon.held_items.items():
                    # Convert underscores to hyphens for item lookup
                    item_lookup_id = item_id.replace("_", "-")
                    # Only copy if item exists in gen4
                    if PokeDBLoader.load_item(item_lookup_id):
                        gen7_held_items[item_id] = versions

                if gen7_held_items != parsed_pokemon.held_items:
                    parsed_pokemon.held_items = gen7_held_items
                    updated = True

                # Set egg cycle to 0
                if parsed_pokemon.hatch_counter != 0:
                    parsed_pokemon.hatch_counter = 0
                    updated = True

                # Save if updated
                if updated:
                    PokeDBLoader.save_pokemon(
                        pokemon_id, parsed_pokemon, subfolder="default"
                    )
                    self.logger.info(f"Updated Pokemon '{pokemon_id}' to gen7 stats")

    def handle_section_change(self, new_section: str) -> None:
        """Handle logic when changing sections.

        Args:
            new_section (str): The new section being entered.
        """
        if new_section == "General Changes":
            self._update_all_pokemon_to_gen7()

        super().handle_section_change(new_section)

    def parse_general_changes(self, line: str) -> None:
        """Parse a line from the General Changes section.

        Args:
            line (str): A line from the General Changes section.
        """
        self.parse_default(line)

    def parse_held_item_exceptions(self, line: str) -> None:
        """Parse a line from the Held Item Exceptions section.

        Args:
            line (str): A line from the Held Item Exceptions section.
        """
        # Matches: - Pokemon has a X% chance to hold a Item.
        if match := re.match(r"^- (.+?) has a (\d+)% chance to hold a (.+?)\.$", line):
            pokemon, chance, item = match.groups()

            # Update the Pokemon's held item
            PokemonItemService.update_held_item(pokemon, item, int(chance))

            # Track this Pokemon to skip later updates in Specific Changes
            pokemon_id = name_to_id(pokemon)
            self._held_item_updated.add(pokemon_id)

            # Format for markdown
            pokemon_md = format_pokemon(pokemon, has_sprite=False)
            item_md = format_item(item)
            self._markdown += (
                f"- {pokemon_md} has a {chance}% chance to hold a {item_md}.\n"
            )
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_other_changes(self, line: str) -> None:
        """Parse a line from the Other Changes section.

        Args:
            line (str): A line from the Other Changes section.
        """
        self.parse_default(line)

    def parse_custom_changes(self, line: str) -> None:
        """Parse a line from the Custom Changes section.

        Args:
            line (str): A line from the Custom Changes section.
        """
        self.parse_default(line)

    def parse_specific_changes(self, line: str) -> None:
        """Parse a line from the Specific Changes section.

        Args:
            line (str): A line from the Specific Changes section.
        """
        next_line = self.peek_line(1) or ""

        # Matches: XXX - Pokemon
        if match := re.match(r"^(\d{3}) - (.+?)$", line):
            number, self._current_pokemon = match.groups()
            self._markdown += f"### {number} {self._current_pokemon}\n\n"
            self._markdown += format_pokemon_card_grid(
                [self._current_pokemon], relative_path="../pokedex/pokemon"
            )
        # Matches: Attribute:
        elif line.endswith(":"):
            self._current_attribute = line[:-1]
            self._markdown += self._format_attribute(
                self._current_attribute, is_changed=next_line.startswith("Old")
            )
        # Matches: Old <value> or New <value>
        elif line.startswith("Old") or line.startswith("New"):
            is_new = line.startswith("New")
            line = line[4:].strip()

            # Format the value if it's an ability or type
            formatted_value = line
            if self._current_attribute.startswith("Ability"):
                formatted_value = self._format_ability_value(line)
            elif self._current_attribute.startswith("Type"):
                formatted_value = self._format_type_value(line)
            elif self._current_attribute.startswith("Base Stats"):
                formatted_value = self._format_base_stats_value(line)

            # Append to markdown table row
            self._markdown += f" {formatted_value} |"
            if not is_new:
                return
            self._markdown += "\n"

            # Update Pokemon attribute in JSON file using AttributeService
            if not self._should_skip_attribute_update():
                AttributeService.update_attribute(
                    pokemon=self._current_pokemon,
                    attribute=self._current_attribute,
                    value=line,
                )
        # Matches: Now compatible with...
        elif self._current_attribute == "Moves" and line.startswith(
            "Now compatible with"
        ):
            # Format for markdown
            formatted_line = self._parse_moves_line(line)
            self._markdown += f"- {formatted_line}\n"
        # Matches: Now able to evolve...
        elif self._current_attribute == "Evolution" and line.startswith(
            "Now able to evolve"
        ):
            # Evolution is handled by evolution_changes_parser, just display as-is
            self._markdown += f"- {line}\n"
        # Matches: Level Up moves (X - Move)
        elif match := re.match(r"^(\d+) - (.*)$", line):
            level = match.group(1)
            move = match.group(2)
            self._markdown += self._format_move_row(level, move)
        # Default: regular text line
        else:
            self.parse_default(line)

    def _should_skip_attribute_update(self) -> bool:
        """Check if we should skip updating the current attribute.

        Returns:
            bool: True if should skip, False otherwise
        """
        # Skip evolution, moves, level up - handled by other parsers/services
        skip_attributes = ["Evolution", "Moves", "Level Up"]
        return any(self._current_attribute.startswith(attr) for attr in skip_attributes)

    def _format_attribute(self, attribute: str, is_changed: bool) -> str:
        """Format an attribute change section.

        Args:
            attribute (str): Attribute name
            is_changed (bool): Whether the attribute has changed.

        Returns:
            str: Formatted markdown for the attribute change section.
        """
        changed_attributes = ["Base Stats", "Type", "Ability", "Catch Rate"]
        md = ""

        if is_changed and any(
            attribute.startswith(attr) for attr in changed_attributes
        ):
            if not self._is_table_open:
                self._is_table_open = True
                md += "| Attribute | Old Value | New Value |\n"
                md += "|:----------|:----------|:----------|\n"
            md += f"| **{self._current_attribute}** | "
            return md

        # Handle static attributes (Evolution, Moves, Held Item)
        static_attributes = ["Evolution", "Moves"]
        if self._is_table_open:
            self._temporary_markdown += f"**{attribute}**:\n\n"
        else:
            md += f"**{attribute}**:\n\n"

        # Level Up moves get a table
        if attribute.startswith("Level Up"):
            md += self._temporary_markdown
            self._temporary_markdown = ""
            self._is_table_open = False
            md += "| Level | Move | Type | Class | Event |\n"
            md += "|:------|:-----|:-----|:------|:------|\n"
        elif attribute in static_attributes:
            pass
        else:
            # Close table if needed for other attributes
            if self._is_table_open:
                self._is_table_open = False

        return md

    def _format_move_row(self, level: str, move: str) -> str:
        """Format a move row for markdown table.

        Args:
            level (str): Level at which the move is learned.
            move (str): Name of the move.

        Returns:
            str: Formatted markdown table row.
        """
        event_move = False
        if move.endswith(" [*]"):
            move = move[:-4]
            event_move = True
        elif move.endswith(" (!!)"):
            move = move[:-5]
            event_move = True

        # Format move name
        move_html = format_move(move)

        # Load move data from PokeDB
        move_data = PokeDBLoader.load_move(move)
        move_type = getattr(move_data.type, VERSION_GROUP, None) if move_data else None
        move_type = move_type.title() if move_type else "Unknown"
        move_class = move_data.damage_class.title() if move_data else "Unknown"

        md = f"| {level} | {move_html} | {format_type_badge(move_type)} | {move_class} | {format_checkbox(event_move)} |\n"
        return md

    def _format_ability_value(self, ability_text: str) -> str:
        """Format ability value with links to individual abilities.

        Args:
            ability_text (str): Ability string in format "Ability1 / Ability2"

        Returns:
            str: Formatted ability string with links
        """
        if not ability_text or ability_text.strip() == "":
            return ability_text

        abilities = [a.strip() for a in ability_text.split("/")]
        formatted_abilities = [
            format_ability(ability)
            for ability in abilities
            if ability.lower() != "none"
        ]

        return " / ".join(formatted_abilities)

    def _format_type_value(self, type_text: str) -> str:
        """Format type value with type badges.

        Args:
            type_text (str): Type string in format "Type1 / Type2"

        Returns:
            str: Formatted type string with badges
        """
        types = [t.strip() for t in type_text.split("/")]
        formatted_types = [format_type_badge(t) for t in types]
        return " ".join(formatted_types)

    def _format_base_stats_value(self, stats_text: str) -> str:
        """Format base stats value.

        Args:
            stats_text (str): Stats string (e.g., "80 HP / 100 Atk / ...")

        Returns:
            str: Formatted stats string
        """
        return f"`{stats_text}`"

    def _parse_moves_line(self, line: str) -> str:
        """Parse TM/HM compatibility line.

        Args:
            line (str): Line to parse.

        Returns:
            str: Formatted line with linked TM/HM for markdown output
        """
        # Skip move tutor lines (not TM/HM)
        if "Move Tutor" in line:
            return line

        # Pattern: "Now compatible with TM56, Weather Ball." or "... (!!)"
        match = re.match(
            r"^Now compatible with (TM|HM)(\d+), (.*?)\.(?: \(!!\)| \[\\?\*\])?$", line
        )
        if not match:
            self.logger.warning(f"Could not parse Moves line: {line}")
            return line

        machine_type = match.group(1)
        number = match.group(2)
        move_name = match.group(3)

        # Format the line with links for markdown output
        tm_item = format_item(f"{machine_type}{number} {move_name}")
        formatted_line = f"Now compatible with {tm_item}."

        # Check if this was an event move
        if line.endswith("(!!)") or line.endswith("[*]"):
            formatted_line += " (!!)"

        return formatted_line
