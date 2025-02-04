from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import json
import logging
import os
import re


def update_tm(tm, old_move, new_move, MOVE_INPUT_PATH, logger):
    old_path = MOVE_INPUT_PATH + format_id(old_move) + ".json"
    new_path = MOVE_INPUT_PATH + format_id(new_move) + ".json"

    old_data = json.loads(load(old_path, logger))
    new_data = json.loads(load(new_path, logger))

    old_data["machines"]["platinum"] = tm.lower()
    new_data["machines"]["platinum"] = tm.lower()

    save(old_path, json.dumps(old_data, indent=4), logger)
    save(new_path, json.dumps(new_data, indent=4), logger)


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    MOVE_INPUT_PATH = os.getenv("MOVE_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Item Changes Parser", LOG_PATH + "item_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "ItemChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Item Changes\n\n"

    listing = False
    parse_table = False

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            if listing:
                md += "\n"
                listing = False
        elif next_line.startswith("="):
            if parse_table:
                md += "\n"
                parse_table = False
            md += f"---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
            listing = True

            if "TM" in line and ">>" in line:
                tm, moves = line[2:].split(": ")
                old_move, new_move = moves.split(" >> ")
                update_tm(tm, old_move, new_move, MOVE_INPUT_PATH, logger)
        elif next_line.startswith("---"):
            headers = re.split(r"\s{3,}", line)
            md += f"| {' | '.join(headers)} |\n"
            parse_table = True
        elif parse_table:
            cells = re.split(r"\s{3,}", line)
            if line.endswith("*"):
                cells[0] = cells[0] + cells.pop(-1)
            cells = ["<br>".join([c[0].upper() + c[1:] for c in cell.split(", ")]) for cell in cells]

            md += f"| {' | '.join(cells)} |\n"
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "item_changes.md", md, logger)


if __name__ == "__main__":
    main()
