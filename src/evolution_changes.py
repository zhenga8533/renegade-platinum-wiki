from dotenv import load_dotenv
from util.file import load, save
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
    logger = Logger("Evolution Changes Parser", LOG_PATH + "evolution_changes.log", LOG)

    # Read input data
    data = load(INPUT_PATH + "EvolutionChanges.txt", logger)
    lines = data.split("\n")
    n = len(lines)
    md = "# Evolution Changes\n\n"

    list_index = 0

    # Parse data
    logger.log(logging.INFO, "Parsing data...")
    for i in range(n):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Parsing line {i + 1}: {line}")

        if line.startswith("=") or line == "":
            continue
        elif next_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
            list_index = 1
        elif line.startswith("- "):
            md += f"{list_index}. {line[2:]}\n"
            list_index += 1
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Data parsed successfully!")

    save(OUTPUT_PATH + "evolution_changes.md", md, logger)


if __name__ == "__main__":
    main()
