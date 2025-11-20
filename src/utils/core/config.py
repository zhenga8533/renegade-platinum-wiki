"""
Configuration constants for the wiki generator.

This module centralizes all configuration values that were previously in config.json.
Values are defined as Python constants for better type safety and easier maintenance.
"""

from typing import Any

# ============================================================================
# PokeDB Configuration
# ============================================================================

POKEDB_REPO_URL = "https://github.com/zhenga8533/pokedb"
POKEDB_BRANCH = "data"
POKEDB_DATA_DIR = "data/pokedb"
POKEDB_GENERATIONS = ["gen4"]
POKEDB_VERSION_GROUPS = ["platinum", "diamond_pearl", "heartgold_soulsilver"]
POKEDB_GAME_VERSIONS = ["platinum", "diamond", "pearl", "heartgold", "soulsilver"]
POKEDB_SPRITE_VERSION = "heartgold_soulsilver"

VERSION_GROUP = "platinum"
VERSION_GROUP_FRIENDLY = "Platinum"
GAME_TITLE = "Renegade Platinum"

# ============================================================================
# Logging Configuration
# ============================================================================

LOGGING_LEVEL = "DEBUG"
LOGGING_FORMAT = "text"
LOGGING_LOG_DIR = "logs"
LOGGING_MAX_LOG_SIZE_MB = 10
LOGGING_BACKUP_COUNT = 5
LOGGING_CONSOLE_COLORS = True
LOGGING_CLEAR_ON_RUN = True

# ============================================================================
# Parser Registry
# ============================================================================

PARSERS_REGISTRY: dict[str, dict[str, Any]] = {
    "evolution_changes": {
        "module": "src.parsers.evolution_changes_parser",
        "class": "EvolutionChangesParser",
        "input_file": "Evolution Changes.txt",
        "output_dir": "docs/changes",
    },
    "item_changes": {
        "module": "src.parsers.item_changes_parser",
        "class": "ItemChangesParser",
        "input_file": "Item Changes.txt",
        "output_dir": "docs/changes",
    },
    "move_changes": {
        "module": "src.parsers.move_changes_parser",
        "class": "MoveChangesParser",
        "input_file": "Move Changes.txt",
        "output_dir": "docs/changes",
    },
    "pokemon_changes": {
        "module": "src.parsers.pokemon_changes_parser",
        "class": "PokemonChangesParser",
        "input_file": "Pokemon Changes.txt",
        "output_dir": "docs/changes",
    },
    "special_events": {
        "module": "src.parsers.special_events_parser",
        "class": "SpecialEventsParser",
        "input_file": "Special Events.txt",
        "output_dir": "docs/reference",
    },
    "trade_changes": {
        "module": "src.parsers.trade_changes_parser",
        "class": "TradeChangesParser",
        "input_file": "Trade Changes.txt",
        "output_dir": "docs/changes",
    },
    "trainer_pokemon": {
        "module": "src.parsers.trainer_pokemon_parser",
        "class": "TrainerPokemonParser",
        "input_file": "Trainer Pokemon.txt",
        "output_dir": "docs/reference",
    },
    "type_changes": {
        "module": "src.parsers.type_changes_parser",
        "class": "TypeChangesParser",
        "input_file": "Type Changes.txt",
        "output_dir": "docs/changes",
    },
    "wild_pokemon": {
        "module": "src.parsers.wild_pokemon_parser",
        "class": "WildPokemonParser",
        "input_file": "Wild Pokemon.txt",
        "output_dir": "docs/reference",
    },
}

PARSER_DEX_RELATIVE_PATH = ".."

# ============================================================================
# Generator Registry
# ============================================================================

GENERATORS_REGISTRY: dict[str, dict[str, Any]] = {
    "pokemon": {
        "module": "src.generators.pokemon_generator",
        "class": "PokemonGenerator",
        "output_dir": "docs/pokedex",
    },
    "abilities": {
        "module": "src.generators.ability_generator",
        "class": "AbilityGenerator",
        "output_dir": "docs/pokedex",
    },
    "items": {
        "module": "src.generators.item_generator",
        "class": "ItemGenerator",
        "output_dir": "docs/pokedex",
    },
    "moves": {
        "module": "src.generators.move_generator",
        "class": "MoveGenerator",
        "output_dir": "docs/pokedex",
    },
    "locations": {
        "module": "src.generators.location_generator",
        "class": "LocationGenerator",
        "output_dir": "docs/locations",
    },
}

GENERATOR_DEX_RELATIVE_PATH = "../.."
GENERATOR_INDEX_RELATIVE_PATH = ".."
