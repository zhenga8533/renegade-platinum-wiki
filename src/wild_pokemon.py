from dotenv import load_dotenv
from util.file import load, save
from util.logger import Logger
import logging
import os
import re


def get_encounter_class(encounter_type: str):
    if encounter_type in ["Morning", "Day", "Night", "Poké Radar"]:
        return "Walking"
    if encounter_type == "Surf":
        return "Surfing"
    if encounter_type in ["Old Rod", "Good Rod", "Super Rod"]:
        return "All Rods"
    return encounter_type


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Wild Pokemon Parser", LOG_PATH + "wild_pokemon.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "WildPokemon.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Wild Pokemon\n"

    rod_levels = {
        "Old Rod": "10",
        "Good Rod": "25",
        "Super Rod": "50",
    }
    levels = rod_levels.copy()

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "" or line == "---":
            pass
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif line.startswith("Levels:"):
            levels = rod_levels.copy()
            for str in line.split(": ", 1)[1].split(", "):
                level, encounter = str.split(" (")
                levels[encounter.rstrip(")")] = level
        elif "%" in line:
            encounter, pokemon = re.split(r"\s{2,}", line)
            level = levels.get(get_encounter_class(encounter), levels.get(encounter, "?"))
            md += f"{encounter} (Lv. {level})\n\n```\n"
            md += "\n".join([f"{i}. {p}" for i, p in enumerate(pokemon.split(", "), 1)]) + "\n```\n\n"
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "wild_pokemon.md", md, logger)


if __name__ == "__main__":
    main()
