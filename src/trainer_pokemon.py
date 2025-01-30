from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite, find_trainer_sprite, format_id
from util.logger import Logger
import logging
import os
import re


def parse_pokemon_set(line: str) -> str:
    strs = [s.strip() for s in line.rstrip("(!)").split("/")]
    name, level, item = re.match(r"(.+) \(Lv\. (\d+)\) @ (.+)", strs[0]).groups()
    nature = strs[1]
    ability = strs[2]
    moves = strs[3].split(", ")
    moves = [moves[i] if len(moves) > i else "—" for i in range(4)]

    pokemon = f"<b>{name}</b> @ {item}\n"
    pokemon += f"<b>Ability:</b> {ability}\n"
    pokemon += f"<b>Level:</b> {level}\n"
    if nature != "?":
        pokemon += f"<b>Nature:</b> {nature}\n"
    pokemon += "<b>Moves:</b>\n"
    pokemon += "\n".join([f"{i}. {move}" for i, move in enumerate(moves, 1)])

    return pokemon + "<br><br>"


def parse_pokemon_table(line: str) -> str:
    strs = [s.strip() for s in line.rstrip("(!)").split("/")]
    name, level, item = re.match(r"(.+) \(Lv\. (\d+)\) @ (.+)", strs[0]).groups()
    nature = strs[1]
    ability = strs[2]
    moves = strs[3].split(", ")
    moves = [moves[i] if len(moves) > i else "—" for i in range(4)]

    sprite = find_pokemon_sprite(name, "front")
    table = f"| {sprite} "
    table = f"| **Lv. {level}** {name}<br>**Ability:** {ability}<br>**Nature:** {nature}<br>**Item:** {item} | "
    table += "<br>".join([f"**{i}.** {move}" for i, move in enumerate(moves, 1)]) + " |\n"

    return table


def parse_trainers(trainers, rematches, important):
    trainers = [t for t in trainers if re.split(r"\s{2,}", t)[0] not in important]
    md = ""
    trainer_rosters = ""
    important_trainers = ""

    if len(trainers) > 0:
        md += "<h3>Generic Trainers</h3>\n\n"
        trainer_rosters += "---\n\n## Generic Trainers\n\n"
        trainer_rosters += "| Trainer | P1 | P2 | P3 | P4 | P5 | P6 |\n"
        trainer_rosters += "|:-------:|:--:|:--:|:--:|:--:|:--:|:--:|\n"

        for trainer in trainers:
            trainer_name, pokemon = re.split(r"\s{2,}", trainer)
            trainer_sprite = find_trainer_sprite(trainer_name, "trainers").replace("../", "../../")

            md += f"1. {trainer_name}"
            trainer_rosters += f"| {trainer_sprite}<br>{trainer_name} "

            for i, p in enumerate(pokemon.split(", "), 1):
                pokemon_name, level = p.split(" Lv. ")
                pokemon_sprite = find_pokemon_sprite(pokemon_name, "front").replace("../", "../../")

                md += f"\n\t{i}. {p}"
                trainer_rosters += f"| {pokemon_sprite}<br>{pokemon_name}<br>Lv. {level} "
            md += "\n"
            trainer_rosters += "|\n"
        md += "\n"

    if len(rematches) > 0:
        md += "<h3>Rematches</h3>\n\n"
        for trainer in rematches:
            name, pokemon = re.split(r"\s{2,}", trainer)
            md += f"1. {name}\n\t"
            md += "\n\t".join([f"{i}. {line}" for i, line in enumerate(pokemon.split(", "), 1)])
            md += "\n"
        md += "\n"

    if len(important) > 0:
        md += "<h3>Important Trainers</h3>\n\n"
        for trainer in important:
            pokemon = important[trainer]
            md += f"**{trainer}**\n\n"
            important_trainers += f"---\n\n## {trainer}\n\n"

            base = ""
            rivals = ["", "", ""]
            rival_index = 0
            elite_four = ["", "", "", ""]
            elite_four_index = 0

            for line in pokemon:
                if line.endswith("(!)"):
                    rivals[rival_index] += parse_pokemon_set(line)
                    rival_index = (rival_index + 1) % 3
                elif trainer.startswith("(R1)"):
                    elite_four[elite_four_index // 6] += parse_pokemon_set(line)
                    elite_four_index += 1
                else:
                    base += parse_pokemon_set(line)

            if rivals[0] != "":
                for i, starter in enumerate(["Turtwig", "Chimchar", "Piplup"]):
                    md += f'=== "{starter}"\n\n\t'
                    md += "\n\t".join(f"<pre><code>{(rivals[i] + base)[:-8]}</code></pre>".split("\n"))
                    md += "\n\n"
            elif elite_four[0] != "":
                for i, num in enumerate(["1", "2", "3", "4"]):
                    md += f'=== "{num}"\n\n\t'
                    md += "\n\t".join(f"<pre><code>{(base + elite_four[i])[:-8]}</code></pre>".split("\n"))
                    md += "\n\n"
            else:
                md += f"<pre><code>{base[:-8]}</code></pre>\n\n"

    return md, trainer_rosters, important_trainers


def main():
    # Load environment variables and logger
    load_dotenv()
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    NAV_OUTPUT_PATH = os.getenv("NAV_OUTPUT_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")

    LOG = os.getenv("LOG") == "True"
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Trainer Pokemon Parser", LOG_PATH + "trainer_pokemon.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "TrainerPokemon.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Trainer Pokémon\n\n"

    trainer = None
    trainers = []
    rematches = []
    important = {}
    roster = trainers

    wild_rosters = {}
    wild_trainers = {}

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            pass
        elif next_line.startswith("="):
            if len(trainers) > 0:
                roster_md, trainer_rosters, important_trainers = parse_trainers(trainers, rematches, important)
                md += roster_md

                location, section = line.split(" (", 1) if "(" in line else (line, None)
                if trainer_rosters != "":
                    wild_rosters[location] = wild_rosters.get(location, "# Trainer Rosters\n\n")
                    wild_rosters[location] += f"---\n\n## {section}\n\n" if section else ""
                    wild_rosters[location] += trainer_rosters
                if important_trainers != "":
                    wild_trainers[location] = wild_trainers.get(location, "# Important Trainers\n\n")
                    wild_trainers[location] += f"---\n\n## {section}\n\n" if section else ""
                    wild_trainers[location] += important_trainers

                trainers = []
                rematches = []
                important = {}
                roster = trainers

            md += f"\n---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"1. {line[2:]}\n"
        elif line == "Rematches":
            roster = rematches
        elif "@" in line:
            important[trainer].append(line)
        elif "@" in next_line:
            trainer = line
            important[trainer] = []
        elif "Lv." in line:
            roster.append(line)
        elif line.startswith("Note:"):
            md += f"!!! note\n\n\t{line[6:]}\n\n"
    # md += parse_trainers(trainers, rematches, important)
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "trainer_pokemon.md", md, logger)

    roster_nav = "  - Wild Encounters:\n"
    trainer_nav = "  - Wild Encounters:\n"
    for location, trainers in wild_rosters.items():
        location_id = format_id(location, symbol="_")
        save(WILD_ENCOUNTER_PATH + location_id + "/trainer_rosters.md", trainers, logger)
        roster_nav += f"      - {location}:\n"
        roster_nav += f"          - Trainer Rosters: {WILD_ENCOUNTER_PATH + location_id}/trainer_rosters.md\n"
    for location, trainers in wild_trainers.items():
        location_id = format_id(location, symbol="_")
        save(WILD_ENCOUNTER_PATH + location_id + "/important_trainers.md", trainers, logger)
        trainer_nav += f"      - {location}:\n"
        trainer_nav += f"          - Important Trainers: {WILD_ENCOUNTER_PATH + location_id}/important_trainers.md\n"
    save(NAV_OUTPUT_PATH + "roster_nav.yml", roster_nav, logger)
    save(NAV_OUTPUT_PATH + "trainer_nav.yml", trainer_nav, logger)


if __name__ == "__main__":
    main()
