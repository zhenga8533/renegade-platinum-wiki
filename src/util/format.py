from util.file import verify_asset_path
from util.logger import Logger
import logging
import re
import string


def find_pokemon_sprite(pokemon: str, view: str, logger: Logger = None) -> str:
    sprite = f"../assets/sprites/{fix_pokemon_form(format_id(pokemon))}/{view}"
    return (
        f"![{pokemon}]({sprite}.gif)" if verify_asset_path(sprite + ".gif", logger) else f"![{pokemon}]({sprite}.png)"
    )


def find_trainer_sprite(trainer: str, view: str, logger: Logger = None) -> str:
    words = trainer.split()
    n = len(words)
    subsets = []

    for i in range(1, 1 << n):  # Iterate through all non-empty subsets
        subset = []
        for j in range(n):
            if i & (1 << j):  # Check if the j-th element is in the subset
                subset.append(words[j])
        subsets.append(" ".join(subset))
    subsets.sort(key=len, reverse=True)

    for subset in subsets:
        sprite = f"../assets/{view}/{format_id(subset, symbol="_")}"
        if verify_asset_path(sprite + ".png", logger):
            return f"![{trainer}]({sprite}.png)"

    if view != "important_trainers":
        return find_trainer_sprite(trainer, "important_trainers", logger)
    return f"![{trainer}](../assets/{view}/{format_id(trainer, symbol="_")}.png)"


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
    Format the ID of a Pokémon.

    :param id: ID to be formatted.
    :return: Formatted ID.
    """

    id = re.sub(r"[^a-zA-Z0-9é\s-]", "", id)
    id = re.sub(r"\s+", " ", id).strip()
    return id.lower().replace(" ", symbol)


def revert_id(id: str, symbol: str = "-") -> str:
    """
    Revert the ID of a Pokémon.

    :param id: ID to be reverted.
    :return: Reverted ID.
    """

    return string.capwords(id.replace(symbol, " "))


def validate_pokemon_form(form: str, logger: Logger) -> bool:
    """
    Verify if a Pokémon form is from this generation.

    :param form: Pokémon form to be validated.
    :return: True if the form is from this generation, False otherwise.
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
        if pokemon in form:
            logger.log(logging.DEBUG, f"Valid form {form} for {pokemon}")
            return True

    logger.log(logging.DEBUG, f"Invalid form {form}")
    return False
