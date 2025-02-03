from dotenv import load_dotenv
from util.file import load
from util.logger import Logger
import glob
import json
import logging
import os


load_dotenv()
ABILITY_INPUT_PATH = os.getenv("ABILITY_INPUT_PATH")

LOG = os.getenv("LOG") == "True"
LOG_PATH = os.getenv("LOG_PATH")
logger = Logger("Ability Loader", LOG_PATH + "ability.log", LOG)

abilities = {}

files = glob.glob(f"{ABILITY_INPUT_PATH}*.json")
for file in files:
    data = json.loads(load(file, logger))
    name = data["name"]
    abilities[name] = data


def get_ability(name: str) -> dict:
    """
    Get the Ability data for an ability.

    :param name: The name of the ability.
    :return: The ability data.
    """

    if name in abilities:
        return abilities[name]
    else:
        logger.log(logging.ERROR, f"Ability {name} not found")
        return None
