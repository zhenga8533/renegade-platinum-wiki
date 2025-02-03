from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite, format_id
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
    logger = Logger("Special Events Parser", LOG_PATH + "special_events.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "SpecialEvents.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Special Events\n"

    parse_encounter = False

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "" or line == "---":
            if parse_encounter and line != "---":
                md += "```\n\n"
                parse_encounter = False
        elif next_line.startswith("="):
            md += f"\n---\n\n## {line}\n\n"
        elif next_line.startswith("---"):
            # Add Pokémon sprites
            md += "\n"
            if line.startswith("#"):
                pokemon = line.split(", ")
                links = []
                sprites = []

                for p in pokemon:
                    pokemon_id = format_id(" ".join(p.split(" ")[1:]))
                    links.append(f"[{p}](../pokemon/{pokemon_id}.md)")
                    sprites.append(find_pokemon_sprite(pokemon_id, "front", logger))

                md += f"**{', '.join(links)}**\n\n"
                md += "\n".join(sprites) + "\n\n"
            else:
                md += f"**{line}**\n\n"

            md += "```\n"
            parse_encounter = True
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif parse_encounter:
            md += line + "\n"
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "special_events.md", md, logger)


if __name__ == "__main__":
    main()
