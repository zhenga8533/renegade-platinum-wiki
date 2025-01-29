from dotenv import load_dotenv
from util.file import load
from util.format import validate_pokemon_form
from util.logger import Logger
import json
import logging
import os
import requests
import threading


def save_sprite(sprite_path: str, sprite: str, logger: Logger) -> None:
    dirs = sprite_path.rsplit("/", 1)[0]
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        logger.log(logging.INFO, f"Created directory '{dirs}'.")

    try:
        with open(sprite_path, "wb") as file:
            file.write(sprite)
            logger.log(logging.INFO, f"The content was saved to '{sprite_path}'.")
    except Exception as e:
        logger.log(logging.ERROR, f"An error occurred while saving to {sprite_path}:\n{e}")
        exit(1)


def fetch_and_save_sprites(pokemon, POKEMON_INPUT_PATH, logger):
    name = pokemon["name"]
    data = json.loads(load(POKEMON_INPUT_PATH + name + ".json", logger))
    species = data["species"]
    id = str(data["id"])
    forms = data.get("forms")

    for form in forms:
        if form != name and not validate_pokemon_form(form, logger):
            continue

        # Official artwork
        sprites = data["sprites"]
        official_artwork = sprites["other"]["official-artwork"]
        official = official_artwork["front_default"]
        official_shiny = official_artwork["front_shiny"]
        sprite_data = {"official": official, "official_shiny": official_shiny}

        # Generation 4, Platinum sprites
        gen_4 = sprites["versions"]["generation-iv"]["platinum"]
        for key in gen_4:
            sprite_name = key.replace("_default", "")
            sprite = gen_4[key]
            if sprite:
                sprite_data[sprite_name] = sprite

        # Fetch all sprites
        for key in sprite_data:
            sprite = sprite_data[key]
            sprite = sprite.replace(id, id + form.replace(species, ""))
            response = requests.get(sprite)
            save_sprite(f"../docs/assets/sprites/{form}/{key}.png", response.content, logger)


def fetch_sprites_for_range(start_index: int, end_index: int, pokedex, POKEMON_INPUT_PATH, logger):
    """
    Fetch and save sprites for a range of Pokémon.

    :param start_index: The starting index for the Pokémon range.
    :param end_index: The ending index for the Pokémon range.
    :param pokedex: The list of Pokémon to process.
    :param POKEMON_INPUT_PATH: Path where Pokémon data is stored.
    :param logger: Logger instance for logging.
    """

    for i in range(start_index, end_index + 1):
        pokemon = pokedex[i]
        fetch_and_save_sprites(pokemon, POKEMON_INPUT_PATH, logger)


def main():
    # Load environment variables and logger
    load_dotenv()
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Sprite Fetcher", LOG_PATH + "sprite_fetcher.log", LOG)

    # Fetch pokedex
    pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=493").json().get("results")

    # Determine the range for each thread
    THREADS = int(os.getenv("THREADS"))
    total_pokemon = len(pokedex)
    chunk_size = total_pokemon // THREADS
    remainder = total_pokemon % THREADS

    threads = []
    start_index = 0

    for t in range(THREADS):
        # Calculate the end index for each thread's range
        end_index = start_index + chunk_size - 1
        if remainder > 0:
            end_index += 1
            remainder -= 1

        # Start each thread to handle a specific range of Pokémon
        thread = threading.Thread(
            target=fetch_sprites_for_range,
            args=(start_index, end_index, pokedex, POKEMON_INPUT_PATH, logger),
        )
        threads.append(thread)
        thread.start()

        # Update the start_index for the next thread
        start_index = end_index + 1

    # Ensure all threads are completed
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
