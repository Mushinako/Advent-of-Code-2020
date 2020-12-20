from pathlib import Path

from aoc_io.aoc_io import DATA_FILENAME, get_input

CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE_PATH = CURRENT_DIR / DATA_FILENAME

if __name__ == "__main__":

    # Download input
    get_input(2020, 12, INPUT_FILE_PATH)

    print(f"Downloaded to {INPUT_FILE_PATH}")
