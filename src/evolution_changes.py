from dotenv import load_dotenv
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
    logger = Logger(LOG, LOG_PATH, logging.INFO, logging.INFO)

    # Read input data


if __name__ == "__main__":
    main()
