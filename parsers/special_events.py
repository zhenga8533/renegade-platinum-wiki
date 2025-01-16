from util.file import load, save


def main():
    content = load("files/SpecialEvents.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    listing = False

    for i in range(n):
        line = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < n else ""
        last_line = lines[i - 1].strip() if i - 1 >= 0 else ""

        if last_line.startswith("=") and next_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
        elif line.startswith("=") or line == "" or line == "---":
            continue
        elif next_line.startswith("- ") and listing:
            md += f"```\n\n"
            listing = False
        elif next_line == "---":
            listing = True
            md += f"---\n\n**{line}**\n\n```\n"
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"

    save("output/special_events.md", md)


if __name__ == "__main__":
    main()
