from util.file import load, save


def main():
    content = load("files/PokemonChanges.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    listing = False
    stating = False

    for i in range(n):
        line = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < n else ""

        if line.startswith("=") or line == "":
            continue
        elif next_line.startswith("=") and " - " in line:
            if listing:
                md += f"</code></pre>\n\n"
                listing = False

            md += f"---\n\n<b>{line}</b>\n\n<pre><code>"
            listing = True
            stating = True
        elif next_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
        elif listing:
            if ":" in line:
                if stating:
                    stating = False
                else:
                    md += "\n"
                md += f"<b>{line}</b>\n"
            else:
                md += f"{line}\n"
        else:
            md += f"{line}\n\n"

    if listing:
        md += f"</code></pre>\n"

    save("output/pokemon_changes.md", md)


if __name__ == "__main__":
    main()
