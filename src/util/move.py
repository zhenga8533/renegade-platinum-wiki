from dotenv import load_dotenv
from util.file import load
from util.format import format_id
from util.logger import Logger
import glob
import json
import logging
import os


load_dotenv()
MOVE_INPUT_PATH = os.getenv("MOVE_INPUT_PATH")

LOG = os.getenv("LOG") == "True"
LOG_PATH = os.getenv("LOG_PATH")
logger = Logger("Move Loader", LOG_PATH + "move.log", LOG)

moves = {}

files = glob.glob(f"{MOVE_INPUT_PATH}*.json")
for file in files:
    data = json.loads(load(file, logger))
    name = format_id(file.split("\\")[-1].split(".")[0])
    moves[name] = data
    logger.log(logging.INFO, f"Loaded move {name}")


def get_move(name: str) -> dict:
    """
    Get the move data for a move.

    :param name: The name of the move.
    :return: The move data.
    """

    id = format_id(name)
    if id in moves:
        return moves[id]
    else:
        logger.log(logging.ERROR, f"Move {id} not found")
        return None
