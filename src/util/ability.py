from dotenv import load_dotenv
from util.file import load
from util.format import format_id
from util.logger import Logger
import glob
import json
import logging
import os


# Load the environment variables and logger.
load_dotenv()
ABILITY_INPUT_PATH = os.getenv("ABILITY_INPUT_PATH")

LOG = os.getenv("LOG") == "True"
LOG_PATH = os.getenv("LOG_PATH")
logger = Logger("Ability Loader", LOG_PATH + "ability.log", LOG)

# Load all the ability data.
abilities = {}

files = glob.glob(f"{ABILITY_INPUT_PATH}*.json")
for file in files:
    data = json.loads(load(file, logger))
    name = format_id(file.split("\\")[-1].split(".")[0])
    abilities[name] = data
    logger.log(logging.INFO, f"Loaded ability {name}")


def get_ability(name: str) -> dict:
    """
    Get the loaded data for an ability.

    :param name: The name of the ability.
    :return: The ability data.
    """

    id = format_id(name)
    if id in abilities:
        return abilities[id]
    else:
        logger.log(logging.ERROR, f"Ability {id} not found")
        return None
