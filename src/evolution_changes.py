from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import glob
import json
import logging
import os


def fix_evolutions(evolutions: list, pokemon: str, change: str) -> list:
    """
    Fix the evolutions list in place by adding the change to the specified pokemon.

    :param evolutions: The list of evolutions to fix.
    :param pokemon: The name of the pokemon to add the change to.
    :param change: The change to add to the specified pokemon.
    :return: All evolutions in the list.
    """

    pokemon_evolutions = []

    for evolution in evolutions:
        name = evolution["name"]
        pokemon_evolutions.append(name)

        if name == pokemon:
            evolution["evolution_changes"] = evolution.get("evolution_changes", []) + [change]

        pokemon_evolutions += fix_evolutions(evolution.get("evolutions", []), pokemon, change)

    return pokemon_evolutions


def fix_pokemon(pokemon: list, evolutions: list, POKEMON_INPUT_PATH: str, logger: Logger) -> None:
    """
    Fix the pokemon list in place by adding the evolution changes to the specified pokemon.

    :param pokemon: The list of pokemon to fix.
    :param evolutions: The list of evolutions to fix.
    :param POKEMON_INPUT_PATH: The path to the pokemon data files.
    :param logger: The logger to use.
    """

    for p in pokemon:
        file_pattern = POKEMON_INPUT_PATH + p + "*.json"
        files = glob.glob(file_pattern)

        # Loop through each Pokémon file
        for file_path in files:
            pokemon_data = json.loads(load(file_path, logger))
            pokemon_data["evolutions"] = evolutions
            save(file_path, json.dumps(pokemon_data, indent=4), logger)


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Evolution Changes Parser", LOG_PATH + "evolution_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "EvolutionChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Evolution Changes\n"

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

            pokemon, change = line[2:].split(": ")
            p = json.loads(load(POKEMON_INPUT_PATH + format_id(pokemon) + ".json", logger))
            evolutions = fix_evolutions(p["evolutions"], format_id(pokemon), change)
            fix_pokemon(evolutions, p["evolutions"], POKEMON_INPUT_PATH, logger)
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "evolution_changes.md", md, logger)


if __name__ == "__main__":
    main()
