from util.logger import Logger
import logging


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
