from dotenv import load_dotenv
from util.file import load, save, verify_asset_path
from util.format import find_pokemon_sprite
from util.logger import Logger
import logging
import os


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Pokemon Changes Parser", LOG_PATH + "pokemon_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "PokemonChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Pokemon Changes\n"

    parse_change = False

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            if parse_change:
                md += "```\n\n"
                parse_change = False
        elif next_line.startswith("="):
            if " - " in line:
                md += f"**#{line}**\n\n"
                pokemon = line.split(" - ")[1]
                md += find_pokemon_sprite(pokemon, "front", logger) + "\n\n"
            else:
                md += f"\n---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif parse_change:
            md += line + "\n"
        elif ":" in line:
            md += line + "\n\n```\n"
            parse_change = True
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "pokemon_changes.md", md, logger)


if __name__ == "__main__":
    main()
