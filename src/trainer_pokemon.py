from dotenv import load_dotenv
from util.file import load, save
from util.logger import Logger
import logging
import os
import re


def parse_pokemon_set(line: str, rival_index: int) -> str:
    if line.startswith("0") or line.startswith("1") or line.startswith("2"):
        if int(line[0]) != rival_index:
            return ""
        line = line[1:].rstrip("(!)")

    strs = [s.strip() for s in line.split("/")]
    name, level, item = re.match(r"(.+) \(Lv\. (\d+)\) @ (.+)", strs[0]).groups()
    nature = strs[1]
    ability = strs[2]
    moves = strs[3].split(", ")

    pokemon = f"<b>{name}</b> @ {item}\n"
    pokemon += f"<b>Ability:</b> {ability}\n"
    pokemon += f"<b>Level:</b> {level}\n"
    pokemon += f"<b>Nature:</b> {nature}\n"
    pokemon += "<b>Moves:</b>\n"
    pokemon += "\n".join([f"{i}. {move}" for i, move in enumerate(moves, 1)])

    return pokemon + "<br><br>"


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Trainer Pokemon Parser", LOG_PATH + "trainer_pokemon.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "TrainerPokemon.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Trainer Pokémon\n\n"

    rivals = ["PKMN Trainer Barry", "PKMN Trainer Dawn", "PKMN Trainer Lucas"]
    trainer_rosters = ["", "", ""]
    rival_index = 0

    curr_trainer = ""
    parse_important = False

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            pass
        elif next_line.startswith("="):
            if parse_important:
                for i in range(3):
                    trainer_rosters[i] = trainer_rosters[i].rstrip("<br>") + "</code></pre>\n\n"
                parse_important = False
            if line == "General Changes":
                md += "---\n\n## General Changes\n\n"
                continue

            for i in range(3):
                if trainer_rosters[i] != "":
                    trainer_rosters[i] += "\n---\n\n"
                trainer_rosters[i] += f"## {line}\n\n"
                trainer_rosters[i] += "<h3>Generic Trainers</h3>\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif line == "Rematches":
            for i in range(3):
                trainer_rosters[i] += "\n<h3>Rematches</h3>\n\n"
        elif "@" in line:
            for i in range(3):
                trainer_rosters[i] += parse_pokemon_set(line, i)
        elif "@" in next_line:
            if not parse_important:
                for i in range(3):
                    trainer_rosters[i] += f"\n<h3>Important Trainers</h3>\n\n"
                parse_important = True
            else:
                for i in range(3):
                    trainer_rosters[i] = trainer_rosters[i].rstrip("<br>") + "</code></pre>\n\n"

            for i in range(3):
                trainer_rosters[i] += f"**{line}**\n\n<pre><code>"
            curr_trainer = line
        elif "Lv." in line:
            trainer, pokemon = re.split(r"\s{2,}", line)
            if trainer != curr_trainer:
                curr_trainer = trainer

            if trainer in rivals:
                trainer_rosters[rival_index] += f"1. {trainer}\n\t"
                trainer_rosters[rival_index] += "\n\t".join([f"1. {p}" for p in pokemon.split(", ")]) + "\n"
                rival_index = (rival_index + 1) % 3
            else:
                for i in range(3):
                    trainer_rosters[i] += f"1. {trainer}\n\t"
                    trainer_rosters[i] += "\n\t".join([f"1. {p}" for p in pokemon.split(", ")]) + "\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    md += "\n---\n\n## Trainer Rosters\n"
    md += '\n=== "Turtwig"\n\n\t'
    md += "\n\t".join(trainer_rosters[0].split("\n")) + "\n"
    md += '\n=== "Chimchar"\n\n\t'
    md += "\n\t".join(trainer_rosters[1].split("\n")) + "\n"
    md += '\n=== "Piplup"\n\n\t'
    md += "\n\t".join(trainer_rosters[2].split("\n")) + "\n"

    save(OUTPUT_PATH + "trainer_pokemon.md", md, logger)


if __name__ == "__main__":
    main()
