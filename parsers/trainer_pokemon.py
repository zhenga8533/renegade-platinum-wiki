from util.file import load, save
from util.pokemon_set import PokemonSet
import re


def main():
    content = load("files/TrainerPokemon.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = False
    training = False

    for i in range(n):
        line = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < n else ""
        last_line = lines[i - 1].strip() if i - 1 >= 0 else ""

        if last_line.startswith("=") and next_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
        elif line.startswith("- "):
            md += f"{line}\n"
        elif line.startswith("=") or line == "":
            if training:
                training = False
                md = md.rstrip() + f"</code></pre>\n\n"
        elif next_line.startswith("=") and len(next_line) > 100:
            md += f"---\n\n#### {line}\n\n"
            listing = True
        elif listing:
            strs = re.split(r" {3,}", line)

            if len(strs) == 1:
                md += f"<sub><b>{line}</b></sub>\n"
                if "/" in next_line:
                    training = True
                    md += f"<pre><code>"
            elif training:
                md += PokemonSet(line).to_string() + "\n"
            else:
                md += f"<sub><b>{strs[0]}</b></sub>\n\n```\n"

                pokemon = strs[1].split(", ")
                for p in pokemon:
                    md += f"{p}\n"
                md += "```\n\n"

    save("output/trainer_pokemon.md", md)


if __name__ == "__main__":
    main()
