from util.file import load, verify_asset_path
from util.logger import Logger
import json
import logging
import os
import re
import string


def find_pokemon_sprite(pokemon: str, view: str, logger: Logger) -> str:
    """
    Find the sprite of a Pokémon.

    :param pokemon: Pokémon to find the sprite.
    :param view: View of the sprite.
    :param logger: Logger to log the verification.
    :return: The sprite of the Pokémon.
    """

    # Load Pokemon data
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    pokemon_id = format_id(pokemon)
    sprite = f"../assets/sprites/{pokemon_id}/{view}"
    file_path = POKEMON_INPUT_PATH + pokemon_id + ".json"
    if not os.path.exists(file_path):
        file_path = file_path.replace(pokemon_id, pokemon_id.rsplit("-", 1)[0])
    pokemon_data = json.loads(load(file_path, logger))
    pokemon_text = pokemon_data["flavor_text_entries"].get("platinum", pokemon).replace("\n", " ")

    return (
        f'![{pokemon}]({sprite}.gif "{pokemon}: {pokemon_text}")'
        if verify_asset_path(sprite + ".gif", logger)
        else (
            f'![{pokemon}]({sprite}.png "{pokemon}: {pokemon_text}")'
            if verify_asset_path(sprite + ".png", logger)
            else "?"
        )
    )


def find_trainer_sprite(trainer: str, view: str, logger: Logger = None) -> str:
    """
    Find the sprite of a trainer.

    :param trainer: Trainer to find the sprite.
    :param view: View of the sprite.
    :param logger: Logger to log the verification.
    :return: The sprite of the trainer.
    """

    words = trainer.split()
    n = len(words)
    subsets = []

    # Iterate through all non-empty subsets
    for i in range(1, 1 << n):
        subset = []
        for j in range(n):
            # Check if the j-th element is in the subset
            if i & (1 << j):
                subset.append(words[j])
        subsets.append(" ".join(subset))
    subsets.sort(key=len, reverse=True)

    # Check if the sprite exists for any subset
    for subset in subsets:
        sprite = f"../assets/{view}/{format_id(subset, symbol="_")}"
        if verify_asset_path(sprite + ".png", logger):
            return f'![{trainer}]({sprite}.png "{trainer}")'

    # Check if the sprite exists for the full name
    if view != "important_trainers":
        return find_trainer_sprite(trainer, "important_trainers", logger)
    return f'![{trainer}](../assets/{view}/{format_id(trainer, symbol="_")}.png "{trainer}")'


def fix_pokemon_form(form: str) -> str:
    """
    Fix the id of a Pokemon with multiple forms.

    :param form: Pokémon form to be fixed.
    :return: Fixed form id.
    """

    if form == "deoxys":
        return "deoxys-normal"
    if form == "wormadam":
        return "wormadam-plant"
    if form == "giratina":
        return "giratina-altered"
    if form == "shaymin":
        return "shaymin-land"
    return form


def format_id(id: str, symbol: str = "-") -> str:
    """
    Format the ID of any string.

    :param id: ID to be formatted.
    :return: Formatted ID.
    """

    id = id.replace("é", "e")
    id = re.sub(r"[^a-zA-Z0-9é\s-]", "", id)
    id = re.sub(r"\s+", " ", id).strip()
    id = id.lower().replace(" ", symbol)
    return fix_pokemon_form(id)


def format_stat(stat: str) -> str:
    """
    Format the name of a stat.

    :param stat: Stat to be formatted.
    :return: Formatted stat.
    """

    stat = format_id(stat)
    if stat == "health":
        return "HP"
    elif stat == "attack":
        return "Atk"
    elif stat == "defense":
        return "Def"
    elif stat == "special-attack":
        return "Sp. Atk"
    elif stat == "special-defense":
        return "Sp. Def"
    elif stat == "speed":
        return "Spd"


def revert_id(id: str, symbol: str = "-") -> str:
    """
    Revert the ID of a Pokémon.

    :param id: ID to be reverted.
    :return: Reverted ID.
    """

    return string.capwords(id.replace(symbol, " "))


def verify_pokemon_form(id: str, logger: Logger) -> bool:
    """
    Verify if a Pokemon form is valid.

    :param id: The ID of the Pokemon.
    :param logger: The logger to use.
    :return: True if the form is valid, False otherwise.
    """

    pokemon_with_forms = [
        "unown",
        "deoxys",
        "castform",
        "burmy",
        "wormadam",
        "cherrim",
        "shellos",
        "gastrodon",
        "rotom",
        "giratina",
        "shaymin",
        "arceus",
    ]

    # Validate if the Pokemon has a form
    for pokemon in pokemon_with_forms:
        if pokemon in id:
            logger.log(logging.DEBUG, f"Valid form {id} for {pokemon}")
            return True

    logger.log(logging.DEBUG, f"Invalid form {id}")
    return False
