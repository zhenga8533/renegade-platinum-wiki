from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite, format_id
from util.logger import Logger
import glob
import json
import logging
import os
import re


def update_pokemon(pokemon_id: str, changes: dict, pokemon_path: str, logger: Logger) -> None:
    """
    Update the Pokémon data for the specified changes.

    :param pokemon_id: The Pokémon to update.
    :param changes: The changes to apply to the Pokémon.
    :param pokemon_path: The path to the Pokémon data files.
    :param logger: The logger to use.
    :return: None
    """

    # Find all Pokémon files that match the specified Pokémon
    file_pattern = pokemon_path + pokemon_id + "*.json"
    files = glob.glob(file_pattern)

    # Loop through each Pokémon file
    for file_path in files:
        data = json.loads(load(file_path, logger))
        if "platinum" not in data["moves"]:
            continue

        # Loop through each change
        for key, value in changes.items():
            # Ability changes
            if key == "abil":
                data["abilities"] = [
                    {"name": format_id(ability), "is_hidden": False, "slot": i}
                    for i, ability in enumerate(value.split(" / "))
                ]
            # Base stat changes
            elif key == "base":
                stats = [int(stat.split(" ")[0]) for stat in value.split(" / ")]
                data["stats"] = {
                    "hp": stats[0],
                    "attack": stats[1],
                    "defense": stats[2],
                    "special-attack": stats[3],
                    "special-defense": stats[4],
                    "speed": stats[5],
                }
            # Base happiness changes
            elif key == "happ":
                data["base_happiness"] = int(value)
            # Pokemon type changes
            elif key == "type" and type(value) == str:
                data["types"] = [t.lower() for t in value.split(" / ")]
            # Machine move changes
            elif key == "move":
                for move in value:
                    machine = "TM" in move or "HM" in move
                    move_id = format_id(move.split(", ")[1] if machine else move.split("with ")[1].split(" from")[0])
                    learn_method = "machine" if machine else "tutor"
                    move_index = next(
                        (
                            i
                            for i, m in enumerate(data["moves"]["platinum"])
                            if m["name"] == move_id and m["learn_method"] == learn_method
                        ),
                        None,
                    )
                    if move_index is not None:
                        continue

                    data["moves"]["platinum"].append(
                        {"name": move_id, "level_learned_at": 0, "learn_method": learn_method}
                    )
            # Level up move changes
            elif key == "leve":
                # Remove all past level up moves
                data["moves"]["platinum"] = [m for m in data["moves"]["platinum"] if m["learn_method"] != "level-up"]

                # Add new level up moves
                for move in value:
                    level, move_name = move.split(" - ")
                    move_id = format_id(move_name)

                    data["moves"]["platinum"].append(
                        {"name": move_id, "level_learned_at": int(level), "learn_method": "level-up"}
                    )

        save(file_path, json.dumps(data, indent=4), logger)


def main():
    """
    Main function for the Pokémon changes parser.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Pokemon Changes Parser", LOG_PATH + "pokemon_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "PokemonChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Pokemon Changes\n"

    parse_change = False
    curr_pokemon = None
    curr_change = None
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
                md += "```\n\n"
                parse_change = False
        # Section headers
        elif next_line.startswith("="):
            if " - " in line:
                pokemon = line.split(" - ")[1]
                pokemon_id = format_id(pokemon)
                md += f"**[#{line}](../pokemon/{pokemon_id}.md)**\n\n"
                md += find_pokemon_sprite(pokemon, "front", logger) + "\n\n"

                if curr_pokemon is not None:
                    update_pokemon(curr_pokemon, changes, POKEMON_INPUT_PATH, logger)
                curr_pokemon = format_id(pokemon)
                changes = {}
            else:
                md += f"\n---\n\n## {line}\n\n"
        # List changes
        elif line.startswith("- "):
            # Held item changes
            item_pattern = r"- ([A-Za-z]+) has a ([0-9]+)% chance to hold a ([A-Z a-z]+)."
            if match := re.match(item_pattern, line):
                # Parse data from the line
                pokemon, chance, item = match.groups()
                pokemon_id = format_id(pokemon)
                chance = int(chance)
                item_id = format_id(item)
                md += f"1. [{pokemon}](../pokemon/{pokemon_id}.md) has a {chance}% chance to hold a {item}.\n"

                # Update Pokémon data
                file_path = POKEMON_INPUT_PATH + pokemon_id + ".json"
                pokemon_data = json.loads(load(file_path, logger))
                held_items = pokemon_data["held_items"]
                if item_id not in held_items:
                    held_items[item_id] = {}
                held_items[item_id]["ultra-sun"] = chance
                held_items[item_id]["ultra-moon"] = chance
                save(file_path, json.dumps(pokemon_data, indent=4), logger)
            # Regular list changes
            else:
                md += f"1. {line[2:]}\n"
        # Code block changes
        elif parse_change:
            md += line + "\n"

            if ": " in line:
                changes[curr_change] = line.split(": ")[1]
            else:
                changes[curr_change] = changes.get(curr_change, []) + [line]
        elif ":" in line:
            md += line + "\n\n```\n"
            parse_change = True
            curr_change = line[0:4].lower() if "Happiness" not in line else "happ"
        # Miscellaneous lines
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "pokemon_changes.md", md, logger)


if __name__ == "__main__":
    main()
