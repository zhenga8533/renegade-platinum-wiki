"""
Configuration for Renegade Platinum Wiki.

This module creates a WikiConfig instance for use throughout the project.
"""

from pathlib import Path

from rom_wiki_core.config import WikiConfig

# Find the project root (where pyproject.toml is located)
_current_file = Path(__file__).resolve()
_package_root = _current_file.parent
PROJECT_ROOT = _package_root.parent.parent

# Create the configuration instance
CONFIG = WikiConfig(
    # Project paths
    project_root=PROJECT_ROOT,
    # Game information
    game_title="Renegade Platinum",
    version_group="platinum",
    version_group_friendly="Platinum",
    # PokeDB configuration
    pokedb_repo_url="https://github.com/zhenga8533/pokedb",
    pokedb_branch="data",
    pokedb_data_dir=str(PROJECT_ROOT / "data" / "pokedb"),
    pokedb_generations=["gen4", "gen7"],
    pokedb_version_groups=["platinum", "diamond_pearl", "heartgold_soulsilver"],
    pokedb_game_versions=["platinum", "diamond", "pearl", "heartgold", "soulsilver"],
    pokedb_sprite_version="heartgold_soulsilver",
    # Logging configuration
    logging_level="DEBUG",
    logging_format="text",
    logging_log_dir=str(PROJECT_ROOT / "logs"),
    logging_max_log_size_mb=10,
    logging_backup_count=5,
    logging_console_colors=True,
    logging_clear_on_run=True,
    # Parser registry (keep your existing parsers)
    parsers_registry={
        "evolution_changes": {
            "module": "renegade_platinum_wiki.parsers.evolution_changes_parser",
            "class": "EvolutionChangesParser",
            "input_file": "Evolution Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "item_changes": {
            "module": "renegade_platinum_wiki.parsers.item_changes_parser",
            "class": "ItemChangesParser",
            "input_file": "Item Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "move_changes": {
            "module": "renegade_platinum_wiki.parsers.move_changes_parser",
            "class": "MoveChangesParser",
            "input_file": "Move Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "pokemon_changes": {
            "module": "renegade_platinum_wiki.parsers.pokemon_changes_parser",
            "class": "PokemonChangesParser",
            "input_file": "Pokemon Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "special_events": {
            "module": "renegade_platinum_wiki.parsers.special_events_parser",
            "class": "SpecialEventsParser",
            "input_file": "Special Events.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "reference"),
        },
        "trade_changes": {
            "module": "renegade_platinum_wiki.parsers.trade_changes_parser",
            "class": "TradeChangesParser",
            "input_file": "Trade Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "trainer_pokemon": {
            "module": "renegade_platinum_wiki.parsers.trainer_pokemon_parser",
            "class": "TrainerPokemonParser",
            "input_file": "Trainer Pokemon.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "reference"),
        },
        "type_changes": {
            "module": "renegade_platinum_wiki.parsers.type_changes_parser",
            "class": "TypeChangesParser",
            "input_file": "Type Changes.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "changes"),
        },
        "wild_pokemon": {
            "module": "renegade_platinum_wiki.parsers.wild_pokemon_parser",
            "class": "WildPokemonParser",
            "input_file": "Wild Pokemon.txt",
            "output_dir": str(PROJECT_ROOT / "docs" / "reference"),
        },
    },
    # Parser configuration
    parser_dex_relative_path="..",
    # Generator registry
    generators_registry={
        "pokemon": {
            "module": "rom_wiki_core.generators.pokemon_generator",
            "class": "PokemonGenerator",
            "output_dir": str(PROJECT_ROOT / "docs" / "pokedex"),
        },
        "abilities": {
            "module": "rom_wiki_core.generators.ability_generator",
            "class": "AbilityGenerator",
            "output_dir": str(PROJECT_ROOT / "docs" / "pokedex"),
        },
        "items": {
            "module": "rom_wiki_core.generators.item_generator",
            "class": "ItemGenerator",
            "output_dir": str(PROJECT_ROOT / "docs" / "pokedex"),
        },
        "moves": {
            "module": "rom_wiki_core.generators.move_generator",
            "class": "MoveGenerator",
            "output_dir": str(PROJECT_ROOT / "docs" / "pokedex"),
        },
        "locations": {
            "module": "rom_wiki_core.generators.location_generator",
            "class": "LocationGenerator",
            "output_dir": str(PROJECT_ROOT / "docs" / "locations"),
        },
    },
    # Generator configuration
    generator_dex_relative_path="../..",
    generator_index_relative_path="..",
    # Location generator configuration
    location_index_columns=["Location", "Trainers", "Wild Encounters"],
)
