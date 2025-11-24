"""
Parser for Item Changes documentation file.

This parser:
1. Reads data/documentation/Item Changes.txt
2. Updates pokemon Item data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/item_changes.md
"""

import re

from src.utils.formatters.markdown_formatter import (
    format_checkbox,
    format_item,
    format_move,
)
from src.utils.formatters.table_formatter import create_table_header
from src.utils.services.item_service import ItemService

from .base_parser import BaseParser


class ItemChangesParser(BaseParser):
    """Parser for  documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs/changes"):
        """Initialize the Item Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs/changes".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = [
            "Modified Items",
            "Modified TMs",
            "Item Locations",
            "TM Locations",
            "Plate Locations",
            "Key Items",
            "Replaced Items",
        ]

        # Modified Items States
        self._is_table_open = False

        # Modified TMs States
        self._is_tm_table_open = False

    def handle_section_change(self, new_section: str) -> None:
        """Handle logic when changing sections.

        Args:
            new_section (str): The new section being entered.
        """
        self._is_table_open = False
        super().handle_section_change(new_section)

    def parse_modified_items(self, line: str) -> None:
        """Parse a line from the Modified Items section.

        Args:
            line (str): A line from the Modified Items section.
        """
        # Matches: - Item Name ($old_price >> $new_price)
        if match := re.match(r"^- (.+?)\s+\(\$(\d+) >> \$(\d+)\)$", line):
            item, old_price, new_price = match.groups()

            # Update the item cost in the database
            ItemService.update_item_cost(item, int(new_price))

            # Format for markdown
            item_md = format_item(item)

            if not self._is_table_open:
                self._markdown += (
                    "| Item | Old Price | New Price |\n"
                    "|:----:|:----------|:----------|\n"
                )
                self._is_table_open = True

            self._markdown += f"| {item_md} | ${old_price} | ${new_price} |\n"
        # Matches: - Item Name (now $0)
        elif line.startswith("- "):
            item_md = format_item(line[2:])
            self._markdown += f"- {item_md}\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_modified_tms(self, line: str) -> None:
        """Parse a line from the Modified TMs section.

        Args:
            line (str): A line from the Modified TMs section.
        """
        # Matches: - TMxx: Old Move >> New Move
        if match := re.match(r"^- (.+?): (.+?) >> (.+?)$", line):
            tm, old_move, new_move = match.groups()

            # Update the TM's move in the database
            ItemService.update_tm_move(tm, new_move)

            if not self._is_tm_table_open:
                self._markdown += (
                    create_table_header(["TM", "Old Move", "New Move"]) + "\n"
                )
                self._is_tm_table_open = True

            self._markdown += f"| {format_item(tm)} | {format_move(old_move)} | {format_move(new_move)} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_item_locations(self, line: str) -> None:
        """Parse a line from the Item Locations section.

        Args:
            line (str): A line from the Item Locations section.
        """
        if line == "Item                    Locations":
            self._markdown += "| Item | Locations |\n"
        elif line == "---                     ---":
            self._markdown += "|:-----|:----------|\n"
        # Matches: Item Name  Locations
        elif match := re.match(r"^(.+?)\s{2,}(.+)$", line):
            item, locations = match.groups()
            self._markdown += f"| {format_item(item)} | {locations} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_tm_locations(self, line: str) -> None:
        """Parse a line from the TM Locations section.

        Args:
            line (str): A line from the TM Locations section.
        """
        if line == "TM                      Location                        Obtained":
            self._markdown += "| TM | Location | Obtained | Changed |\n"
        elif line == "---                     ---                             ---":
            self._markdown += "|:---|:---------|:---------|:-------:|\n"
        # Matches: TM Name  Location  Obtained
        elif match := re.match(r"^(.+?)\s{2,}(.+?)\s{2,}(.+)$", line):
            tm, location, obtained = match.groups()

            changed = False
            if obtained.endswith("*"):
                changed = True
                obtained = obtained[:-1].strip()

            self._markdown += f"| {format_item(tm)} | {location} | {obtained} | {format_checkbox(changed)} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_plate_locations(self, line: str) -> None:
        """Parse a line from the Plate Locations section.

        Args:
            line (str): A line from the Plate Locations section.
        """
        if line == "Item                    Master Trainer Location":
            self._markdown += "| Item | Master Trainer Location |\n"
        elif line == "---                     ---":
            self._markdown += "|:-----|:------------------------|\n"
        # Matches: Item Name  Location
        elif match := re.match(r"^(.+?)\s{2,}(.+)$", line):
            item, location = match.groups()
            self._markdown += f"| {format_item(item)} | {location} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_key_items(self, line: str) -> None:
        """Parse a line from the Key Items section.

        Args:
            line (str): A line from the Key Items section.
        """
        if line == "Item                    Location                            Method":
            self._markdown += "| Item | Location | Method | Changed | New |\n"
        elif line == "---                     ---                                 ---":
            self._markdown += "|:-----|:---------|:-------|:-------:|:---:|\n"
        # Matches: Item Name  Location  Method
        elif match := re.match(r"^(.+?)\s{2,}(.+?)\s{2,}(.+)$", line):
            item, location, method = match.groups()

            changed = False
            is_new = False
            if method.endswith("**"):
                is_new = True
                method = method[:-2].strip()
            elif method.endswith("*"):
                changed = True
                method = method[:-1].strip()

            self._markdown += f"| {format_item(item)} | {location} | {method} | {format_checkbox(changed)} | {format_checkbox(is_new)} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)

    def parse_replaced_items(self, line: str) -> None:
        """Parse a line from the Replaced Items section.

        Args:
            line (str): A line from the Replaced Items section.
        """
        if line == "Old Item                New Item":
            self._markdown += "| Old Item | New Item |\n"
        elif line == "---------               ---------":
            self._markdown += "|:---------|:---------|\n"
        # Matches: Old Item  New Item
        elif match := re.match(r"^(.+?)\s{2,}(.+)$", line):
            old_item, new_item = match.groups()
            self._markdown += f"| {format_item(old_item)} | {format_item(new_item)} |\n"
        # Default: regular text line
        else:
            self.parse_default(line)
