"""
Parser package for processing documentation files.
"""

from .evolution_changes_parser import EvolutionChangesParser
from .item_changes_parser import ItemChangesParser
from .move_changes_parser import MoveChangesParser
from .pokemon_changes_parser import PokemonChangesParser
from .special_events_parser import SpecialEventsParser
from .trade_changes_parser import TradeChangesParser
from .trainer_pokemon_parser import TrainerPokemonParser
from .type_changes_parser import TypeChangesParser
from .wild_pokemon_parser import WildPokemonParser

__all__ = [
    "EvolutionChangesParser",
    "ItemChangesParser",
    "MoveChangesParser",
    "PokemonChangesParser",
    "SpecialEventsParser",
    "TradeChangesParser",
    "TrainerPokemonParser",
    "TypeChangesParser",
    "WildPokemonParser",
]
