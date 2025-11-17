"""
Parser for Evolution Changes documentation file.

This parser:
1. Reads data/documentation/EvolutionChanges.txt
2. Updates pokemon evolution data in data/pokedb/parsed/
3. Generates a markdown file to docs/evolution_changes.md
"""

from .base_parser import BaseParser


class EvolutionChangesParser(BaseParser):
    """Parser for Evolution Changes documentation.

    Args:
        BaseParser (_type_): Abstract base parser class
    """

    def __init__(self, input_file: str, output_dir: str = "docs"):
        """Initialize the Evolution Changes parser.

        Args:
            input_file (str): Path to the input file.
            output_dir (str, optional): Path to the output directory. Defaults to "docs".
        """
        super().__init__(input_file=input_file, output_dir=output_dir)
        self._sections = ["Item Interaction Changes", "Level Changes", "Method Changes"]

    def parse_(self, line: str) -> None:
        """Parse a line from the General Notes section.

        Args:
            line (str): A line from the General Notes section.
        """
        self.parse_default(line)
