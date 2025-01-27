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
    logger = Logger("Item Changes Parser", LOG_PATH + "item_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "ItemChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Item Changes\n"

    list_index = 1
    parse_table = False

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            continue
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
            parse_table = False
        elif line.startswith("- "):
            md += f"{list_index}. {line[2:]}\n"
            list_index += 1
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
            if list_index > 1:
                md += "\n"
                list_index = 1
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "item_changes.md", md, logger)


if __name__ == "__main__":
    main()
