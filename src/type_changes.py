from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite
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
    logger = Logger("Type Changes Parser", LOG_PATH + "type_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "TypeChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Type Changes\n"

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            pass
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif next_line.startswith("---"):
            headers = re.split(r"\s{3,}", line)
            headers.insert(1, "ID")
            md += f"| {' | '.join(headers)} |\n"
        elif line.startswith("---"):
            seperators = re.split(r"\s{3,}", line)
            seperators.insert(1, "---")
            md += f"| {' | '.join(seperators)} |\n"
        else:
            cells = re.split(r"\s{3,}", line)
            pokemon = " ".join(cells[0].split(" ")[1:])
            cells[0] = "<br>".join(cells[0].split(" "))
            cells[1] = "<br>".join(cells[1].split(" / "))
            cells[2] = "<br>".join(cells[2].split(" / "))
            cells[-1] = "<br>".join([c[0].upper() + c[1:] for c in cells[-1].split("; ")]).rstrip(".")

            md += f"| {find_pokemon_sprite(pokemon, 'front', logger)} | "
            md += " | ".join(cells) + " |\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "type_changes.md", md, logger)


if __name__ == "__main__":
    main()
