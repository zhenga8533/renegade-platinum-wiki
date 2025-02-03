from dotenv import load_dotenv
from util.file import load
from util.logger import Logger
import glob
import json
import logging
import os


load_dotenv()
MOVES_INPUT_PATH = os.getenv("MOVES_INPUT_PATH")

LOG = os.getenv("LOG") == "True"
LOG_PATH = os.getenv("LOG_PATH")
logger = Logger("Move Loader", LOG_PATH + "moves.log", LOG)

moves = {}

files = glob.glob(f"{MOVES_INPUT_PATH}*.json")
for file in files:
    data = json.loads(load(file, logger))
    name = data["name"]
    moves[name] = data


def get_move(name: str) -> dict:
    """
    Get the move data for a move.

    :param name: The name of the move.
    :return: The move data.
    """

    if name in moves:
        return moves[name]
    else:
        logger.log(logging.ERROR, f"Move {name} not found")
        return None
