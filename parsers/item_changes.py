from util.file import load, save
import re


def main():
    content = load("files/ItemChanges.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    modify = False
    listing = False
    tabling = False

    for i in range(n):
        line = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < n else ""
        last_line = lines[i - 1].strip() if i > 0 else ""

        if line.startswith("Modified"):
            md += f"---\n\n## {line}\n\n"
            modify = True
        elif last_line.startswith("=") and next_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
            tabling = True
            modify = False
        elif modify:
            if line.startswith("-"):
                if not listing:
                    listing = True
                    md += "```\n"

                md += f"{line}\n"
            elif line != "" and not line.startswith("="):
                md += f"**{line}**\n\n"
            elif listing:
                md += "```\n\n"
                listing = False
        elif tabling:
            if next_line.startswith("---"):
                listing = True

            if line.startswith("="):
                continue
            elif line == "":
                md += "\n"
                listing = False
            elif listing:
                strs = re.split(r"\s{3,}", line)
                if re.fullmatch(r"\*+", strs[-1]):
                    strs[0] = strs[0] + strs.pop(-1)
                strs = [
                    (
                        "<br>".join(f"{i+1}. {item}" for i, item in enumerate(s.split(", ")))
                        if len(s.split(", ")) > 1
                        else s
                    )
                    for s in strs
                ]

                md += f"| {' | '.join(strs)} |\n"
            else:
                md += f"{line}\n\n"

    save("output/item_changes.md", md)


if __name__ == "__main__":
    main()
