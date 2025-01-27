from dotenv import load_dotenv
from util.file import load, save
from util.logger import Logger
import logging
import os
import re


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")

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
        elif next_line.startswith("="):
            if parse_table:
                md += "\n"
                parse_table = False
            md += f"---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += line + "\n"
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
            old = "<br>".join(old.split(" + "))
            new = "<br>".join(new.split(" + "))
            md += f"| {attribute} | {old} | {new} |\n"
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "move_changes.md", md, logger)


if __name__ == "__main__":
    main()
