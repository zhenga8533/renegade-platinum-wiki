from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import json
import logging
import os
import re


def update_move(move, changes, MOVES_INPUT_PATH, logger):
    data = json.loads(load(MOVES_INPUT_PATH + move + ".json", logger))

    for key, value in changes.items():
        if key == "effect":
            if value == "High Critical Ratio":
                data["effect"] = (
                    "Inflicts regular damage. User's critical hit rate is one level higher when using this move."
                )
            elif value.startswith("No Effect"):
                data["effect"] = "Inflicts regular damage."
            elif value.startswith("Burn"):
                chance = value.split(" ")[1]
                data["effect"] = (
                    "Inflicts regular damage. Thaws the user if frozen and has a {chance} chance to burn the target."
                )
            elif value.startswith("May Raise Attack"):
                chance = value.split(" ")[-1]
                data["effect"] = (
                    f"Inflicts regular damage. Has a {chance} chance to raise the user's Attack one stage."
                )
        elif key == "recovery":
            percent = value.split(" ")[0]
            data["effect"] = f"Deals regular damage. Drains {percent} of the damage inflicted to heal the user."
        elif key in data:
            data[key] = value
        else:
            logger.log(logging.WARNING, f"Attribute {key} not found in move {move}!")

    save(MOVES_INPUT_PATH + move + ".json", json.dumps(data, indent=4), logger)


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    MOVES_INPUT_PATH = os.getenv("MOVES_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Move Changes Parser", LOG_PATH + "move_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "MoveChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Move Changes\n\n"

    parse_table = False
    parse_change = False

    curr_move = None
    changes = {}

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            if parse_change:
                md += "\n"
                parse_change = False
            if curr_move:
                update_move(curr_move, changes, MOVES_INPUT_PATH, logger)
                curr_move = None
                changes = {}
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
            parse_table = False
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif next_line.startswith("---"):
            headers = re.split(r"\s{3,}", line)
            md += f"| {' | '.join(headers)} |\n"
            parse_table = True
        elif parse_table:
            cells = re.split(r"\s{3,}", line)
            md += f"| {' | '.join(cells)} |\n"
        elif ">>" in line:
            if not parse_change:
                md += "| Attribute | Old | New |\n"
                md += "| --------- | --- | --- |\n"
                parse_change = True

            attribute, change = line.split(": ")
            old, new = change.split(" >> ")
            changes[attribute.lower()] = new

            old = "<br>".join(old.split(" + "))
            new = "<br>".join(new.split(" + "))
            md += f"| {attribute} | {old} | {new} |\n"
        elif ">>" in next_line:
            curr_move = format_id(line)
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "move_changes.md", md, logger)


if __name__ == "__main__":
    main()
