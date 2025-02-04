from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import json
import logging
import os
import re


def update_move(move: str, changes: dict, move_path: str, logger: Logger) -> None:
    """
    Update the move data for the specified move.

    :param move: The move to update.
    :param changes: The changes to apply to the move.
    :param move_path: The path to the move data files.
    :param logger: The logger to use.
    :return: None
    """

    data = json.loads(load(move_path + move + ".json", logger))

    # Update the move data
    for key, value in changes.items():
        # Preset effect changes
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
        # Recovery effect changes
        elif key == "recovery":
            percent = value.split(" ")[0]
            data["effect"] = f"Deals regular damage. Drains {percent} of the damage inflicted to heal the user."
        # Other changes
        elif key in data:
            data[key] = value
        # Log warning if attribute not found
        else:
            logger.log(logging.WARNING, f"Attribute {key} not found in move {move}!")

    save(move_path + move + ".json", json.dumps(data, indent=4), logger)


def replace_move(old_move: str, new_move: str, move_path: str, logger: Logger) -> None:
    """
    Replace the old move with the new move in the move data files.

    :param old_move: The old move to replace.
    :param new_move: The new move to replace with.
    :param move_path: The path to the move data files.
    :param logger: The logger to use.
    :return: None
    """

    new_data = json.loads(load(move_path + format_id(new_move) + ".json", logger))
    save(move_path + format_id(old_move) + ".json", json.dumps(new_data, indent=4), logger)


def main():
    """
    Main function for the move changes parser.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    MOVE_INPUT_PATH = os.getenv("MOVE_INPUT_PATH")

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

        # Skip empty lines
        if line.startswith("=") or line == "":
            if parse_change:
                md += "\n"
                parse_change = False
            if curr_move:
                update_move(curr_move, changes, MOVE_INPUT_PATH, logger)
                curr_move = None
                changes = {}
        # Section headers
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
            parse_table = False
        # List changes
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        # Table headers
        elif next_line.startswith("---"):
            headers = re.split(r"\s{3,}", line)
            md += f"| {' | '.join(headers)} |\n"
            parse_table = True
        # Table data
        elif parse_table:
            cells = re.split(r"\s{3,}", line)
            md += f"| {' | '.join(cells)} |\n"
            if not cells[0].startswith("---"):
                replace_move(cells[0], cells[1], MOVE_INPUT_PATH, logger)
        # Move change headers
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
        # Move change data
        elif ">>" in next_line:
            curr_move = format_id(line)
        # Miscellaneous lines
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "move_changes.md", md, logger)


if __name__ == "__main__":
    main()
