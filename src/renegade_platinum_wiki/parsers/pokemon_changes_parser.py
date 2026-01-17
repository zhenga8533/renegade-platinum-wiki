"""
Parser for Pokemon Changes documentation file.

This parser:
1. Reads data/documentation/Pokemon Changes.txt
2. Updates pokemon data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/pokemon_changes.md
"""

import re

import orjson
from rom_wiki_core.parsers.base_parser import BaseParser
from rom_wiki_core.utils.core.loader import PokeDBLoader
from rom_wiki_core.utils.data.models import MoveLearn, Pokemon, PokemonAbility, Stats
from rom_wiki_core.utils.formatters.markdown_formatter import (
    format_checkbox,
    format_item,
    format_move,
    format_pokemon,
    format_pokemon_card_grid,
    format_type_badge,
)
from rom_wiki_core.utils.services.attribute_service import AttributeService
from rom_wiki_core.utils.services.pokemon_item_service import PokemonItemService
from rom_wiki_core.utils.services.pokemon_move_service import PokemonMoveService
from rom_wiki_core.utils.text.text_util import name_to_id

from renegade_platinum_wiki.config import CONFIG


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
        self._current_forme = ""  # Track current forme (e.g., "Normal Forme", "Attack Forme")
        self._is_table_open = False

        # Track moves for current Pokemon
        self._move_markdown = ""
        self._levelup_moves: list[tuple[int, str]] = []  # list of (level, move ID)
        self._machine_moves: list[str] = []  # list of move IDs
        self._tutor_moves: list[str] = []  # list of move IDs

        # Track attribute changes for current Pokemon
        self._new_abilities: list[str] = []  # list of ability names
        self._new_stats: Stats | None = None  # new base stats
        self._new_types: list[str] = []  # list of type names
        self._new_catch_rate: int | None = None  # new catch rate

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
            pokemon_id = name_to_id(pokemon)
            item_id = name_to_id(item)

            # Update the Pokemon's held item
            PokemonItemService.update_held_item(pokemon_id, item_id, int(chance))

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
            self._apply_pokemon_changes()

            number, self._current_pokemon = match.groups()
            self._markdown += f"### {number} {self._current_pokemon}\n\n"
            self._markdown += (
                format_pokemon_card_grid(
                    [self._current_pokemon], relative_path="../pokedex/pokemon"
                )
                + "\n\n"
            )

            self._is_table_open = False
        # Matches: Attribute:
        elif line.endswith(":") and next_line.startswith("Old"):
            if not self._is_table_open:
                self._markdown += "| Attribute | Old Value | New Value |\n"
                self._markdown += "|:----------|:----------|:----------|\n"
                self._is_table_open = True

            self._current_attribute = line[:-1]
            self._markdown += f"| **{line[:-1]}** |"
        elif line.startswith("Old"):
            old_value = line[4:].strip()
            self._markdown += f" {old_value} |"
        elif line.startswith("New"):
            new_value = line[4:].strip()
            self._markdown += f" {new_value} |\n"
            self._parse_new_attribute_value(new_value)
        # Matches: Attribute: (without old value, for moves)
        elif line.endswith(":") and not next_line.startswith("Old"):
            self._current_attribute = line[:-1]
            self._move_markdown += f"\n**{line[:-1]}:**\n\n"

            if line.startswith("Level Up"):
                # Check if this is a forme-specific Level Up section
                new_forme = self._extract_forme(line[:-1])

                # If forme changed and we have pending moves, apply them first
                if new_forme != self._current_forme and self._levelup_moves:
                    self._apply_levelup_moves()

                # Update current forme
                self._current_forme = new_forme

                self._move_markdown += "| Level | Move | Type | Class | Event |\n"
                self._move_markdown += "|:------|:-----|:-----|:------|:------|\n"
        # Matches: Now compatible with TM##, Move Name.
        elif match := re.match(r"^Now compatible with (?:HM|TM)\d+, ([^.]+).*$", line):
            self._move_markdown += f"- {line}\n"
            self._machine_moves.append(name_to_id(match.group(1)))
        # Matches: Now compatible with Move Name from the Move Tutor.
        elif match := re.match(
            r"^Now compatible with (.+?) from the Move Tutor.*$", line
        ):
            self._move_markdown += f"- {line}\n"
            self._tutor_moves.append(name_to_id(match.group(1)))
        elif match := re.match(r"^(\d+) - (.+?)$", line):
            level, move = match.groups()
            move_data = PokeDBLoader.load_move(move)
            if not move_data:
                self.logger.warning(f"Move not found for level-up move: {move}")
                return

            type_badge = format_type_badge(
                getattr(move_data.type, CONFIG.version_group)
            )
            move_class = move_data.damage_class
            event_check = format_checkbox("!!" in line)

            self._move_markdown += f"| {level} | {format_move(move)} | {type_badge} | {move_class} | {event_check} |\n"
            self._levelup_moves.append((int(level), name_to_id(move)))

            if next_line == "":
                self._move_markdown += "\n"

    def _extract_forme(self, attribute: str) -> str:
        """Extract forme name from an attribute string.

        Args:
            attribute (str): The attribute string (e.g., "Level Up (Normal Forme)").

        Returns:
            str: The forme name (e.g., "normal") or empty string if no forme.
        """
        # Match forme patterns like "(Normal Forme)", "(Attack Forme)", "(Plant Forme)"
        if match := re.search(r"\(([^)]+\s+Forme)\)", attribute):
            forme_name = match.group(1)
            # Convert "Normal Forme" -> "normal", "Attack Forme" -> "attack"
            forme_id = forme_name.replace(" Forme", "").lower()
            # "Regular Forme" refers to the base form (no suffix)
            if forme_id == "regular":
                return ""
            return forme_id
        return ""

    def _get_pokemon_id_with_forme(self, forme: str = "") -> str:
        """Get the pokemon ID, optionally with forme suffix.

        Args:
            forme (str): The forme name (e.g., "normal", "attack").

        Returns:
            str: The pokemon ID with forme suffix if applicable.
        """
        pokemon_id = name_to_id(self._current_pokemon)
        if forme:
            return f"{pokemon_id}-{forme}"
        return pokemon_id

    def _parse_new_attribute_value(self, value: str) -> None:
        """Parse and store a new attribute value based on current attribute.

        For attributes with formes (stats, types, abilities), immediately applies
        the change to the forme-specific pokemon ID.

        Args:
            value (str): The new value string to parse.
        """
        attr_lower = self._current_attribute.lower()
        forme = self._extract_forme(self._current_attribute)

        # Parse ability changes: "Ability1 / Ability2" or "Ability1 / None"
        if "ability" in attr_lower and (
            "complete" in attr_lower or "classic" not in attr_lower
        ):
            abilities_raw = [a.strip() for a in value.split("/")]
            # Filter out "None" entries
            ability_names = [a for a in abilities_raw if a.lower() != "none"]

            if forme:
                # Immediately apply to forme-specific pokemon
                pokemon_id = self._get_pokemon_id_with_forme(forme)
                abilities: list[PokemonAbility] = []
                for i, ability_name in enumerate(ability_names, start=1):
                    is_hidden = i == 3
                    abilities.append(
                        PokemonAbility(
                            name=name_to_id(ability_name), is_hidden=is_hidden, slot=i
                        )
                    )
                AttributeService.update_abilities(pokemon_id, abilities)
            else:
                self._new_abilities = ability_names

        # Parse base stat changes: "80 HP / 82 Atk / 83 Def / 100 SAtk / 100 SDef / 80 Spd / 525 BST"
        elif "base stats" in attr_lower:
            stat_pattern = r"(\d+)\s*HP\s*/\s*(\d+)\s*Atk\s*/\s*(\d+)\s*Def\s*/\s*(\d+)\s*SAtk\s*/\s*(\d+)\s*SDef\s*/\s*(\d+)\s*Spd"
            if match := re.match(stat_pattern, value):
                hp, atk, defense, spatk, spdef, speed = map(int, match.groups())
                stats = Stats(
                    hp=hp,
                    attack=atk,
                    defense=defense,
                    special_attack=spatk,
                    special_defense=spdef,
                    speed=speed,
                )
                if forme:
                    pokemon_id = self._get_pokemon_id_with_forme(forme)
                    AttributeService.update_base_stats(pokemon_id, stats)
                else:
                    self._new_stats = stats

        # Parse type changes: "Fire / Dragon" or "Fire"
        elif "type" in attr_lower:
            types = [t.strip().lower() for t in value.split("/")]
            if forme:
                pokemon_id = self._get_pokemon_id_with_forme(forme)
                AttributeService.update_type(pokemon_id, types)
            else:
                self._new_types = types

        # Parse catch rate changes: "45"
        elif "catch rate" in attr_lower:
            catch_rate = int(value)
            if forme:
                pokemon_id = self._get_pokemon_id_with_forme(forme)
                AttributeService.update_catch_rate(pokemon_id, catch_rate)
            else:
                self._new_catch_rate = catch_rate

    def _apply_levelup_moves(self) -> None:
        """Apply level-up moves for the current Pokemon and forme."""
        if not self._levelup_moves or self._current_pokemon == "":
            return

        pokemon_id = self._get_pokemon_id_with_forme(self._current_forme)
        move_learns = [
            MoveLearn(
                name=move_id,
                level_learned_at=level,
                version_groups=[CONFIG.version_group],
            )
            for level, move_id in self._levelup_moves
        ]
        PokemonMoveService.update_levelup_moves(pokemon_id, move_learns)
        self._levelup_moves = []

    def _apply_pokemon_changes(self) -> None:
        """Apply all tracked changes for the current Pokemon using services."""
        if self._current_pokemon == "":
            return

        pokemon_id = name_to_id(self._current_pokemon)

        # Apply ability changes (non-forme specific)
        if self._new_abilities:
            abilities: list[PokemonAbility] = []
            for i, ability_name in enumerate(self._new_abilities, start=1):
                # Slot 3 is hidden ability
                is_hidden = i == 3
                abilities.append(
                    PokemonAbility(
                        name=name_to_id(ability_name), is_hidden=is_hidden, slot=i
                    )
                )
            AttributeService.update_abilities(pokemon_id, abilities)

        # Apply stat changes (non-forme specific)
        if self._new_stats:
            AttributeService.update_base_stats(pokemon_id, self._new_stats)

        # Apply type changes (non-forme specific)
        if self._new_types:
            AttributeService.update_type(pokemon_id, self._new_types)

        # Apply catch rate changes (non-forme specific)
        if self._new_catch_rate is not None:
            AttributeService.update_catch_rate(pokemon_id, self._new_catch_rate)

        # Apply any remaining level-up moves (with current forme)
        self._apply_levelup_moves()

        # Apply machine (TM/HM) moves
        if self._machine_moves:
            PokemonMoveService.update_move_category(
                pokemon_id, "machine", self._machine_moves
            )

        # Apply tutor moves
        if self._tutor_moves:
            PokemonMoveService.update_move_category(
                pokemon_id, "tutor", self._tutor_moves
            )

        # Append move markdown and reset all tracking variables
        self._markdown += self._move_markdown
        self._move_markdown = ""
        self._levelup_moves = []
        self._machine_moves = []
        self._tutor_moves = []
        self._new_abilities = []
        self._new_stats = None
        self._new_types = []
        self._new_catch_rate = None
        self._current_forme = ""

    def finalize(self) -> None:
        self._apply_pokemon_changes()
        return super().finalize()
