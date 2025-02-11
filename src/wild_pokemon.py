from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite, format_id
from util.logger import Logger
import logging
import os
import re


def get_encounter_class(encounter_type: str):
    """
    Get the encounter class for the specified encounter type.

    :param encounter_type: The encounter type to get the class for.
    :return: The encounter class for the specified encounter type.
    """

    if encounter_type in ["Morning", "Day", "Night", "Poké Radar"]:
        return "Walking"
    if encounter_type == "Surf":
        return "Surfing"
    if encounter_type in ["Old Rod", "Good Rod", "Super Rod"]:
        return "Fishing"
    return encounter_type


def main():
    """
    Main function for the wild pokemon parser.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    NAV_OUTPUT_PATH = os.getenv("NAV_OUTPUT_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Wild Pokemon Parser", LOG_PATH + "wild_pokemon.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "WildPokemon.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Wild Pokemon\n\n"
    md += "!!! tip\n\n\tFor a more comprehensive list of wild Pokémon encounters, please refer to the [Wild Encounters](../wild_encounters/twinleaf_town/wild_pokemon.md) page.\n\n"

    rod_levels = {
        "Old Rod": "10",
        "Good Rod": "25",
        "Super Rod": "50",
    }
    levels = rod_levels.copy()

    curr_location = None
    curr_encounter = None
    wild_encounters = {}

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        # Skip empty lines
        if line.startswith("=") or line == "" or line == "---":
            pass
        # Section headers
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"

            # Set wild encounters for the current location
            curr_location, section = line.split(" (", 1) if "(" in line else (line, None)
            wild_encounters[curr_location] = wild_encounters.get(
                curr_location, f"# {curr_location} — Wild Pokémon\n\n"
            )
            wild_encounters[curr_location] += f"---\n\n## {section[:-1]}\n\n" if section else ""
            curr_encounter = None
        # List changes
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        # Encounter levels
        elif line.startswith("Levels:"):
            levels = rod_levels.copy()
            for str in line.split(": ", 1)[1].split(", "):
                level, encounter = str.split(" (")
                levels[encounter.rstrip(")")] = level
        # Wild Pokémon encounters
        elif "%" in line:
            encounter, pokemon = re.split(r"\s{2,}", line)
            encounter_class = get_encounter_class(encounter)
            level = levels.get(encounter_class, levels.get(encounter, "?"))
            wild_pokemon = pokemon.split(", ")

            md += f"{encounter} (Lv. {level})\n\n<pre><code>"
            for i, p in enumerate(wild_pokemon, 1):
                p, chance = p.split(" (")
                md += f"{i}. <a href='/renegade-platinum-wiki/pokemon/{format_id(p)}/'>{p}</a> ({chance[:-1]})\n"
            md += "</code></pre>\n\n"

            # Add wild encounters to the current location
            if curr_encounter != encounter_class:
                wild_encounters[curr_location] += f"### {encounter_class}\n\n"
                wild_encounters[curr_location] += f"| Sprite | Pokémon | Encounter Type | Level | Chance |\n"
                wild_encounters[curr_location] += f"|:------:|---------|:--------------:|-------|--------|\n"
                curr_encounter = encounter_class

            # Loop through wild Pokemon encounters
            for wild in wild_pokemon:
                pokemon, chance = wild.split(" (")
                pokemon_id = format_id(pokemon)
                sprite = find_pokemon_sprite(pokemon, "front", logger).replace("../", "../../")
                encounter_type = f'![{encounter}](../../assets/encounter_types/{format_id(encounter, symbol="_")}.png "{encounter}")'

                wild_encounters[curr_location] = wild_encounters[curr_location].rstrip() + "\n"
                wild_encounters[curr_location] += f"| {sprite} | [{pokemon}](../../pokemon/{pokemon_id}.md/) | "
                wild_encounters[curr_location] += f"{encounter_type}{{: style='max-width: 24px;' }} | "
                wild_encounters[curr_location] += f"{level} | {chance[:-1]} |\n"
            wild_encounters[curr_location] += "\n"
        # Miscellaneous lines
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "wild_pokemon.md", md, logger)

    # Save wild encounters navigation
    nav = "  - Wild Encounters:\n"
    for location, encounters in wild_encounters.items():
        location_id = format_id(location, symbol="_")
        save(WILD_ENCOUNTER_PATH + location_id + "/wild_pokemon.md", encounters, logger)
        nav += f"      - {location}:\n"
        nav += f"          - Wild Pokémon: {WILD_ENCOUNTER_PATH + location_id}/wild_pokemon.md\n"
    save(NAV_OUTPUT_PATH + "wild_nav.yml", nav, logger)


if __name__ == "__main__":
    main()
