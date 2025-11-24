"""
Parser for Pokemon Changes documentation file.

This parser:
1. Reads data/documentation/Pokemon Changes.txt
2. Updates pokemon Item data in data/pokedb/parsed/
3. Generates a markdown file to docs/changes/pokemon_changes.md
"""

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
        self._sections = [""]

    def parse_(self, line: str) -> None:
        """Parse a line from the .

        Args:
            line (str): A line from the .
        """
        self.parse_default(line)
