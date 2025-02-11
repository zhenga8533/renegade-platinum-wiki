from dotenv import load_dotenv
from util.ability import get_ability
from util.file import load, save, verify_asset_path
from util.format import find_pokemon_sprite, format_id, revert_id, verify_pokemon_form
from util.item import get_item
from util.logger import Logger
from util.move import get_move
import glob
import json
import logging
import os
import requests


def parse_sprite_tables(
    title: str,
    name: str,
    extension: str,
    logger: Logger,
):
    """
    Parse the sprite tables for a Pokémon.

    :param title: The title of the sprite tables.
    :param name: The name of the Pokémon.
    :param extension: The extension of the sprite files.
    :param logger: The logger to use.
    :return: The parsed sprite tables.
    """

    md = "### " + title + "\n\n"
    md += "| Front | Shiny | Back | Shiny |\n"
    md += "|-------|-------|------|-------|\n|"

    pokemon = revert_id(name)
    sprites = [
        find_pokemon_sprite(pokemon, f"front{extension}", logger),
        find_pokemon_sprite(pokemon, f"front_shiny{extension}", logger),
        find_pokemon_sprite(pokemon, f"back{extension}", logger),
        find_pokemon_sprite(pokemon, f"back_shiny{extension}", logger),
    ]
    valid = False

    for sprite in sprites:
        if sprite == "":
            md += " N/A |"
            continue
        valid = True
        md += f" {sprite} |"

    if not valid:
        return ""
    else:
        md += "\n\n"

    return md


def parse_evolution_line(evolution: dict, pokemon_set: set, level: int = 1, index: int = 1) -> str:
    """
    Parse the evolution line for a Pokémon.

    :param evolution: The evolution data to parse.
    :param pokemon_set: The set of valid Pokémon names.
    :param level: The current level of the evolution.
    :param index: The current index of the evolution.
    :return: The parsed evolution line.
    """

    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    names = [evolution["name"]]

    # Add alternate forms to the evolution line
    for name in names[:]:
        if name not in pokemon_set:
            names.remove(name)
            file_pattern = f"{POKEMON_INPUT_PATH + name}*.json"
            files = glob.glob(file_pattern)

            for file_path in files:
                new_name = file_path.split("\\")[-1].split(".")[0]
                if new_name != name and new_name in pokemon_set and new_name not in names:
                    names.append(new_name)
    if len(names) == 0:
        return ""

    # Recursively parse the full evolution line
    md = ""
    for name in names:
        md += f"{'    ' * (level - 1)}{index}. "
        evolution_details = evolution["evolution_details"]
        if len(evolution_details) > 0:
            md += revert_id(evolution_details[-1]["trigger"]["name"]) + ": "
        md += f"[{revert_id(name)}]({name}.md/)\n"

        if evolution["evolutions"]:
            for i, sub_evolution in enumerate(evolution["evolutions"], 1):
                md += parse_evolution_line(sub_evolution, pokemon_set, level + 1, i)
        md += "\n"

    return md


def calculate_hp(base: int, iv: int, ev: int, level: int) -> int:
    """
    Calculate the HP stat for a Pokémon.

    :param base: The base HP stat.
    :param iv: The IVs of the Pokémon.
    :param ev: The EVs of the Pokémon.
    :param level: The level of the Pokémon.
    :return: The calculated HP stat
    """

    return int(((2 * base + iv + ev // 4) * level) // 100 + level + 10)


def calculate_stat(base: int, iv: int, ev: int, level: int, nature: float) -> int:
    """
    Calculate a stat for a Pokémon besides HP.

    :param base: The base stat.
    :param iv: The IVs of the Pokémon.
    :param ev: The EVs of the Pokémon.
    :param level: The level of the Pokémon.
    :param nature: The nature multiplier.
    :return: The calculated stat
    """

    return int((((2 * base + iv + ev // 4) * level) // 100 + 5) * nature)


def parse_stats(stats: dict) -> str:
    """
    Parse the base stats for a Pokémon.

    :param stats: The base stats to parse.
    :return: The parsed base stats.
    """

    md = "---\n\n## Base Stats\n"
    hp = stats["hp"]
    attack = stats["attack"]
    defense = stats["defense"]
    sp_attack = stats["special-attack"]
    sp_defense = stats["special-defense"]
    speed = stats["speed"]
    md += f"|   | HP | Attack | Defense | Sp. Atk | Sp. Def | Speed |\n"
    md += f"|---|----|--------|---------|---------|---------|-------|\n"
    md += f"| **Base** | {hp} | {attack} | {defense} | {sp_attack} | {sp_defense} | {speed} |\n"
    md += f"| **Min** "
    md += f"| {calculate_hp(hp, 0, 0, 100)} "
    md += f"| {calculate_stat(attack, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(defense, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(sp_attack, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(sp_defense, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(speed, 0, 0, 100, 0.9)} |\n"
    md += f"| **Max** "
    md += f"| {calculate_hp(hp, 31, 252, 100)} "
    md += f"| {calculate_stat(attack, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(defense, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(sp_attack, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(sp_defense, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(speed, 31, 252, 100, 1.1)} |\n\n"
    md += "The ranges shown above are for a level 100 Pokémon. "
    md += "Maximum values are based on a beneficial nature, 252 EVs, 31 IVs; "
    md += "minimum values are based on a hindering nature, 0 EVs, 0 IVs.\n\n"

    return md


def parse_moves(moves: list, headers: list, move_key: str, input_path: str, logger: Logger) -> str:
    """
    Parse the moves for a Pokémon.

    :param moves: The moves to parse.
    :param headers: The headers for the move table.
    :param move_key: The key for the move data.
    :param input_path: The path to the move data.
    :param logger: The logger to use.
    :return: The parsed moves.
    """

    md_header = f"| {' | '.join(headers).strip()} |"
    md_separator = f"| {' | '.join(['---'] * len(headers)).strip()} |"
    md_body = ""
    dash = "\u2014"

    # Parse each move into Markdown table format
    for move in moves:
        move_id = format_id(move["name"])
        move_data = get_move(move_id)
        for category in headers:
            if category == "Lv.":
                md_body += f"| {move['level_learned_at']} "
            elif category == "TM":
                md_body += f"| {move_data['machines'].get(move_key, "tbd").upper()} "
            elif category == "Move":
                move_id = move_data["name"]
                move_data = get_move(move_id)
                move_effect = move_data["flavor_text_entries"].get("platinum", move_data["effect"]).replace("\n", " ")
                md_body += f'| <span class="tooltip" title="{move_effect}">{revert_id(move_id)}</span> '
            elif category == "Type":
                move_type = move_data["type"]
                md_body += (
                    f'| ![{move_type}](../assets/types/{move_type.lower()}.png "{move_type.title()}"){{: width="48"}} '
                )
            elif category == "Cat.":
                damage_class = move_data["damage_class"]
                md_body += f'| ![{move_data["damage_class"]}](../assets/move_category/{damage_class}.png "{damage_class.title()}"){{: width="36"}} '
            elif category == "Power":
                md_body += f"| {move_data['power'] or dash} "
            elif category == "Acc.":
                md_body += f"| {move_data['accuracy'] or dash} "
            elif category == "PP":
                md_body += f"| {move_data['pp']} "
        md_body += "|\n"

    return f"{md_header}\n{md_separator}\n{md_body}\n"


def to_md(pokemon: dict, pokemon_set: dict, logger: Logger) -> str:
    """
    Convert Pokémon data to a readable Markdown format.

    :param pokemon: The Pokémon data to convert.
    :param pokemon_set: The set of valid Pokémon names.
    :param logger: The logger to use.
    :return: The Pokémon data in Markdown format.
    """

    # Basic information
    name_id = pokemon["name"]
    pokemon_name = revert_id(name_id)
    pokemon_id = pokemon["id"]
    md = (
        f"# {pokemon_name} ({pokemon['genus']})\n\n"
        if pokemon_id > 10000
        else f"# #{pokemon_id:03} {pokemon_name} ({pokemon['genus']})\n\n"
    )

    # Add official artwork
    md += "| Official Artwork | Shiny Artwork |\n"
    md += "|------------------|---------------|\n"
    md += f'| ![Official Artwork](../assets/sprites/{name_id}/official.png "{revert_id(name_id)}") | '
    md += f'![Shiny Artwork](../assets/sprites/{name_id}/official_shiny.png "{revert_id(name_id)}") |\n\n'

    # Add flavor text
    flavor_text = pokemon["flavor_text_entries"]["platinum"]
    md += flavor_text.replace("\n", " ") + "\n\n"

    # Add sprite tables
    md += "---\n\n## Media\n\n"
    md += parse_sprite_tables("Default Sprites", name_id, "", logger)
    md += parse_sprite_tables("Female Sprites", name_id, "_female", logger)
    for form in pokemon["forms"]:
        if form == name_id or form in pokemon_set or not verify_pokemon_form(form, logger):
            continue
        md += parse_sprite_tables(f"{revert_id(form)} Sprites", form, "", logger)

    # Cries
    md += "### Cries\n\n"
    latest_cry = f"../assets/cries/{name_id}/latest.ogg"
    legacy_cry = f"../assets/cries/{name_id}/legacy.ogg"
    latest_exists = verify_asset_path(latest_cry, logger)
    legacy_exists = verify_asset_path(legacy_cry, logger)

    if latest_exists:
        md += "Latest (Gen VI+):\n\n<audio controls>\n"
        md += f"<source src='../{latest_cry}' type='audio/ogg'>\n"
        md += "  Your browser does not support the audio element.\n"
        md += "</audio>\n\n"
    if legacy_exists:
        md += "Legacy:\n\n<audio controls>\n"
        md += f"<source src='../{legacy_cry}' type='audio/ogg'>\n"
        md += "  Your browser does not support the audio element.\n"
        md += "</audio>\n\n"
    if not latest_exists and not legacy_exists:
        md += "No cries available.\n\n"

    # Pokédex data
    md += "---\n\n## Pokédex Data\n\n"
    md += f"| National № | Type(s) | Height | Weight | Abilities | Local № |\n"
    md += f"|------------|---------|--------|--------|-----------|---------|\n"
    md += f"| #{pokemon_id}"
    md += f" | " + " ".join(
        [f'![{t}](../assets/types/{t.lower()}.png "{t.title()}"){{: width="48"}}' for t in pokemon["types"]]
    )
    md += f" | {pokemon['height']} m /<br>{pokemon['height'] * 3.28084:.1f} ft"
    md += f" | {pokemon['weight']} kg /<br>{pokemon['weight'] * 2.20462:.1f} lbs"

    abilities = []
    for i, ability in enumerate(pokemon["abilities"], 1):
        ability_id = ability["name"]
        if ability_id == "none":
            continue

        ability_data = get_ability(ability_id)
        ability_effect = ability_data["flavor_text_entries"].get("platinum", ability_data["effect"]).replace("\n", " ")
        abilities.append(f'{i}. <span class="tooltip" title="{ability_effect}">{revert_id(ability_id)}</span>')
    md += f" | " + "<br>".join(abilities)

    local_no = pokemon["pokedex_numbers"].get("original-sinnoh", None)
    md += f" | {'#' + str(local_no) if local_no else 'N/A'} |\n\n"

    # Stats
    stats = pokemon["stats"]
    md += parse_stats(stats)

    # Forms
    md += "---\n\n## Forms & Evolutions\n\n"
    md += '!!! warning "WARNING"\n\n'
    md += "    Information on evolutions may not be 100% accurate;"
    md += " differences between evolution methods across generations are not accounted for.\n\n"

    md += "### Forms\n\n"
    forms = []

    for i, form in enumerate(pokemon["forms"]):
        if form in pokemon_set:
            forms.append(f"{i + 1}. [{revert_id(form)}]({form}.md/)\n")
    if len(forms) == 1:
        md += f"{pokemon_name} has no alternate forms.\n\n"
    else:
        md += "\n".join(forms) + "\n\n"

    # Evolutions
    md += "### Evolution Line\n\n"
    evolutions = pokemon["evolutions"]
    if len(evolutions) == 0:
        md += f"{pokemon_name} does not evolve.\n\n"
    else:
        md += f"{parse_evolution_line(evolutions[0], pokemon_set)}\n\n"

    if "evolution_changes" in pokemon and len(pokemon["evolution_changes"]) > 0:
        md += f"### Evolution Changes\n\n"
        for i, change in enumerate(pokemon["evolution_changes"]):
            md += f"{i + 1}. {change}\n"
        md += "\n"

    # Training
    md += "---\n\n## Training\n\n"
    md += f"| EV Yield | Catch Rate | Base Friendship | Base Exp. | Growth Rate | Held Items |\n"
    md += f"|----------|------------|-----------------|-----------|-------------|------------|\n"
    ev_yield = pokemon["ev_yield"]
    md += f"| " + "<br>".join([f"{ev_yield[stat]} {revert_id(stat)}" for stat in ev_yield if ev_yield[stat] > 0])
    md += " | " + str(pokemon["capture_rate"])
    md += " | " + str(pokemon["base_happiness"])
    md += " | " + str(pokemon["base_experience"])
    md += " | " + revert_id(pokemon["growth_rate"]) + " | "

    held_items = pokemon["held_items"]
    if len(held_items) == 0:
        md += f"N/A |\n\n"
    else:
        for item in held_items:
            item_rarity = held_items[item]
            item_data = get_item(item)
            if item_data is None:
                logger.log(logging.WARNING, f"Item {item} not found in PokéAPI")
                continue
            if "generation-iv" not in item_data["games"] or "ultra-sun" not in item_rarity:
                logger.log(logging.WARNING, f"Item {item} not found in Generation IV games")
                continue

            item_effect = item_data["flavor_text_entries"].get("platinum", item_data["effect"]).replace("\n", " ")
            md += f'<span class="tooltip" title="{item_effect}">{revert_id(item)}</span> ({item_rarity["ultra-sun"]}%)<br>'
        md = md[:-4] + " |\n\n"

    # Breeding
    md += "---\n\n## Breeding\n\n"
    md += f"| Egg Groups | Egg Cycles | Gender | Dimorphic | Color | Shape |\n"
    md += f"|------------|------------|--------|-----------|-------|-------|\n"
    md += f"| " + "<br>".join([f"{i + 1}. {group.title()}" for i, group in enumerate(pokemon["egg_groups"])])
    md += " | " + str(pokemon["hatch_counter"])
    female_rate = pokemon["female_rate"]
    md += " | " + (
        "Genderless"
        if female_rate == -1
        else f"{(8 - female_rate) / 8 * 100}% Male<br>{female_rate / 8 * 100}% Female"
    )
    md += " | " + str(pokemon["has_gender_differences"])
    md += " | " + pokemon["color"].title()
    md += " | " + pokemon["shape"].title()
    md += " |\n\n"

    # Gen 4 Platinum Moves
    level_up_moves = []
    tm_moves = []
    egg_moves = []
    tutor_moves = []

    moves = pokemon["moves"]
    move_keys = list(moves.keys())
    move_key = "platinum" if "platinum" in move_keys else move_keys[-1] if len(move_keys) > 0 else ""
    moves = moves.get(move_key, [])

    for move in moves:
        if move["learn_method"] == "level-up":
            level_up_moves.append(move)
        elif move["learn_method"] == "machine":
            tm_moves.append(move)
        elif move["learn_method"] == "egg":
            egg_moves.append(move)
        elif move["learn_method"] == "tutor":
            tutor_moves.append(move)

    # Moves
    md += "---\n\n## Moves\n\n"
    md += '!!! warning "WARNING"\n\n'
    md += "    Specific move information may be incorrect. "
    md += "However, the general movepool should be accurate; this includes changes made in Renegade Platinum.\n\n"
    MOVE_INPUT_PATH = os.getenv("MOVE_INPUT_PATH")

    # Level Up Moves
    md += "### Level Up Moves\n\n"
    if len(level_up_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by leveling up.\n"
    else:
        level_up_moves.sort(key=lambda x: (x["level_learned_at"], x["name"]))
        md += parse_moves(
            level_up_moves, ["Lv.", "Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, MOVE_INPUT_PATH, logger
        )

    # TM Moves
    md += "### TM Moves\n\n"
    if len(tm_moves) == 0:
        md += f"{pokemon_name} cannot learn any TM moves.\n"
    else:
        tm_moves_data = []
        for move in tm_moves:
            move_data = get_move(move["name"])
            tm_moves_data.append(move_data)
        tm_moves_data.sort(key=lambda x: x["machines"].get(move_key, "ZZZ"))
        md += parse_moves(
            tm_moves_data, ["TM", "Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, MOVE_INPUT_PATH, logger
        )

    # Egg Moves
    md += "### Egg Moves\n\n"
    if len(egg_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by breeding.\n"
    else:
        md += parse_moves(
            egg_moves, ["Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, MOVE_INPUT_PATH, logger
        )

    # Tutor Moves
    md += "### Tutor Moves\n\n"
    if len(tutor_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves from tutors.\n"
    else:
        md += parse_moves(
            tutor_moves, ["Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, MOVE_INPUT_PATH, logger
        )

    return md


def main():
    """
    Main function for the Pokémon parser.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    TIMEOUT = int(os.getenv("TIMEOUT"))
    LOG_PATH = os.getenv("LOG_PATH")
    NAV_OUTPUT_PATH = os.getenv("NAV_OUTPUT_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    POKEMON_PATH = os.getenv("POKEMON_PATH")
    logger = Logger("Pokémon Parser", f"{LOG_PATH}pokemon.log", LOG)

    # Fetch Pokémon data from PokéAPI
    try:
        logger.log(logging.INFO, "Fetching Pokémon data from PokéAPI")
        pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=493", timeout=TIMEOUT).json()[
            "results"
        ]
        logger.log(logging.INFO, "Successfully fetched Pokémon data from PokéAPI")
    except requests.exceptions.RequestException:
        logger.log(logging.ERROR, "Failed to fetch Pokémon data from PokéAPI")
        exit(1)

    # Fetch all valid Pokémon paths
    logger.log(logging.INFO, "Fetching all valid Pokémon paths")
    pokemon_set = set()
    species = []
    forms = []

    for pokemon in pokedex:
        name = pokemon["name"]
        file_pattern = f"{POKEMON_INPUT_PATH + name.split('-')[0]}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            new_name = file_path.split("\\")[-1].split(".")[0]

            if new_name == name:
                species.append(new_name)
                pokemon_set.add(new_name)
            elif verify_pokemon_form(new_name, logger):
                forms.append(new_name)
                pokemon_set.add(new_name)

    # Remove duplicate forms
    for form in forms[:]:
        if form in species:
            forms.remove(form)
    logger.log(logging.INFO, "Successfully fetched all valid Pokémon paths")

    # Generate nav for mkdocs.yml
    logger.log(logging.INFO, "Generating Pokémon navigation")
    generations = ["Kanto", "Johto", "Hoenn", "Sinnoh"]
    pokedex_start = [0, 151, 251, 386]
    nav = ""

    for i, name in enumerate(species):
        if i in pokedex_start:
            nav += f"      - {generations[pokedex_start.index(i)]}:\n"

        clean_name = revert_id(name)
        nav += f'          - "#{f"{i + 1:03}"} {clean_name}": {POKEMON_PATH + name}.md\n'
    nav += f"      - Pokémon Forms:\n"
    for name in forms:
        clean_name = revert_id(name)
        nav += f"          - {clean_name}: {POKEMON_PATH + name}.md\n"

    logger.log(logging.INFO, "Successfully generated Pokémon navigation")
    save(f"{NAV_OUTPUT_PATH}pokemon_nav.md", nav, logger)

    # Generate markdown files for each Pokémon
    logger.log(logging.INFO, "Generating markdown files for each Pokémon")
    for pokemon in pokedex:
        name = pokemon["name"]
        file_pattern = f"{POKEMON_INPUT_PATH + name.split('-')[0]}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            data = json.loads(load(file_path, logger))
            form_name = data["name"]
            if form_name not in pokemon_set:
                continue

            md = to_md(data, pokemon_set, logger)
            save(f"{POKEMON_PATH + data['name']}.md", md, logger)


if __name__ == "__main__":
    main()
