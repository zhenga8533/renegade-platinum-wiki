from dotenv import load_dotenv
from util.file import load
from util.format import verify_pokemon_form
from util.logger import Logger
import json
import logging
import os
import requests
import threading


def save_media(media_path: str, media: str, logger: Logger) -> None:
    """
    Save the media content to the specified path.

    :param media_path: The path to save the media content.
    :param media: The media content to save.
    :param logger: The logger to use.
    :return: None
    """

    # Create the directory if it does not exist
    dirs = media_path.rsplit("/", 1)[0]
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        logger.log(logging.INFO, f"Created directory '{dirs}'.")

    # Save the media content to the specified path
    try:
        with open(media_path, "wb") as file:
            file.write(media)
            logger.log(logging.INFO, f"The content was saved to '{media_path}'.")
    except Exception as e:
        logger.log(logging.ERROR, f"An error occurred while saving to {media_path}:\n{e}")
        exit(1)


def fetch_media(pokemon: dict, pokemon_path: str, logger: Logger) -> None:
    """
    Fetch and save media for the specified Pokémon.

    :param pokemon: The Pokémon to fetch media for.
    :param pokemon_path: The path to the Pokémon data files.
    :param logger: The logger to use.
    :return: None
    """

    # Load the Pokémon data
    name = pokemon["name"]
    data = json.loads(load(pokemon_path + name + ".json", logger))
    forms = data.get("forms")

    # Fetch media for each form
    for form in forms:
        if form != name and not verify_pokemon_form(form, logger):
            continue

        form_data = load(pokemon_path + form + ".json", logger)
        form_data = json.loads(form_data) if form_data != "" else data

        # Official artwork
        sprites = form_data["sprites"]
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

        # Save all sprites
        for key in sprite_data:
            sprite = sprite_data[key]
            logger.log(logging.INFO, f"Fetching sprite for {form} from {sprite}.")
            response = requests.get(sprite)
            save_media(f"../docs/assets/sprites/{form}/{key}.png", response.content, logger)

        # Save cries
        cries = {
            "latest": form_data["cry_latest"] or form_data["cry_legacy"],
            "legacy": form_data["cry_legacy"] or form_data["cry_latest"],
        }
        for key in cries:
            cry = cries[key]
            if cry is None:
                continue

            logger.log(logging.INFO, f"Fetching cry for {form} from {cry}.")
            response = requests.get(cry)
            save_media(f"../docs/assets/cries/{form}/{key}.ogg", response.content, logger)


def fetch_media_range(start_index: int, end_index: int, pokedex: list, pokemon_path: str, logger: Logger) -> None:
    """
    Fetch and save media for a range of Pokémon.

    :param start_index: The starting index for the Pokémon range.
    :param end_index: The ending index for the Pokémon range.
    :param pokedex: The list of Pokémon to process.
    :param pokemon_path: Path where Pokémon data is stored.
    :param logger: Logger instance for logging.
    """

    for i in range(start_index, end_index + 1):
        pokemon = pokedex[i]
        fetch_media(pokemon, pokemon_path, logger)


def main():
    """
    Main function for the media fetcher.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Media Fetcher", LOG_PATH + "media_fetcher.log", LOG)

    # Fetch pokedex
    pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=493").json().get("results")
    logger.log(logging.INFO, pokedex)

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
            target=fetch_media_range,
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
