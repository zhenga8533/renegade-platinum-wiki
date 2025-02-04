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
ITEM_INPUT_PATH = os.getenv("ITEM_INPUT_PATH")

LOG = os.getenv("LOG") == "True"
LOG_PATH = os.getenv("LOG_PATH")
logger = Logger("Item Loader", LOG_PATH + "item.log", LOG)

# Load all the item data.
items = {}

files = glob.glob(f"{ITEM_INPUT_PATH}*.json")
for file in files:
    data = json.loads(load(file, logger))
    name = format_id(file.split("\\")[-1].split(".")[0])
    items[name] = data
    logger.log(logging.INFO, f"Loaded item {name}")


def get_item(name: str) -> dict:
    """
    Get the item data for a item.

    :param name: The name of the item.
    :return: The item data.
    """

    id = format_id(name)
    if id in items:
        return items[id]
    else:
        logger.log(logging.ERROR, f"Item {id} not found")
        return None
