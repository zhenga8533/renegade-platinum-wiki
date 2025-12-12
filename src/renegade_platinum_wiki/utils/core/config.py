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
POKEDB_GENERATIONS = ["gen4", "gen7"]
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
        "module": "renegade_platinum_wiki.parsers.evolution_changes_parser",
        "class": "EvolutionChangesParser",
        "input_file": "Evolution Changes.txt",
        "output_dir": "docs/changes",
    },
    "item_changes": {
        "module": "renegade_platinum_wiki.parsers.item_changes_parser",
        "class": "ItemChangesParser",
        "input_file": "Item Changes.txt",
        "output_dir": "docs/changes",
    },
    "move_changes": {
        "module": "renegade_platinum_wiki.parsers.move_changes_parser",
        "class": "MoveChangesParser",
        "input_file": "Move Changes.txt",
        "output_dir": "docs/changes",
    },
    "pokemon_changes": {
        "module": "renegade_platinum_wiki.parsers.pokemon_changes_parser",
        "class": "PokemonChangesParser",
        "input_file": "Pokemon Changes.txt",
        "output_dir": "docs/changes",
    },
    "special_events": {
        "module": "renegade_platinum_wiki.parsers.special_events_parser",
        "class": "SpecialEventsParser",
        "input_file": "Special Events.txt",
        "output_dir": "docs/reference",
    },
    "trade_changes": {
        "module": "renegade_platinum_wiki.parsers.trade_changes_parser",
        "class": "TradeChangesParser",
        "input_file": "Trade Changes.txt",
        "output_dir": "docs/changes",
    },
    "trainer_pokemon": {
        "module": "renegade_platinum_wiki.parsers.trainer_pokemon_parser",
        "class": "TrainerPokemonParser",
        "input_file": "Trainer Pokemon.txt",
        "output_dir": "docs/reference",
    },
    "type_changes": {
        "module": "renegade_platinum_wiki.parsers.type_changes_parser",
        "class": "TypeChangesParser",
        "input_file": "Type Changes.txt",
        "output_dir": "docs/changes",
    },
    "wild_pokemon": {
        "module": "renegade_platinum_wiki.parsers.wild_pokemon_parser",
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
        "module": "renegade_platinum_wiki.generators.pokemon_generator",
        "class": "PokemonGenerator",
        "output_dir": "docs/pokedex",
    },
    "abilities": {
        "module": "renegade_platinum_wiki.generators.ability_generator",
        "class": "AbilityGenerator",
        "output_dir": "docs/pokedex",
    },
    "items": {
        "module": "renegade_platinum_wiki.generators.item_generator",
        "class": "ItemGenerator",
        "output_dir": "docs/pokedex",
    },
    "moves": {
        "module": "renegade_platinum_wiki.generators.move_generator",
        "class": "MoveGenerator",
        "output_dir": "docs/pokedex",
    },
    "locations": {
        "module": "renegade_platinum_wiki.generators.location_generator",
        "class": "LocationGenerator",
        "output_dir": "docs/locations",
    },
}

GENERATOR_DEX_RELATIVE_PATH = "../.."
GENERATOR_INDEX_RELATIVE_PATH = ".."
