#!/usr/bin/env python3
"""
Get input from and submit answer to AOC
"""

# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
# pyright: reportOptionalMemberAccess=false

from time import sleep
from string import Template
from pathlib import Path
from typing import Literal, Union

import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

DATA_FILENAME = "input.txt"
TOKEN_FILENAME = "token.txt"
TOKEN_PATH = Path(__file__).parent / TOKEN_FILENAME

DATA_URL = Template("https://adventofcode.com/${year}/day/${day}/input")
ANSWER_URL = Template("https://adventofcode.com/${year}/day/${day}/answer")

with TOKEN_PATH.open("r") as token_fp:
    token_value = token_fp.readline().strip()

COOKIES = {"session": token_value}


def get_input(
    year: int,
    day: int,
    input_path: Path,
) -> None:
    """
    Download input from AOC website

    Args:
        year       (int)         : The year of AOC
        day        (1..25)       : The day of AOC
        input_path (pathlib.Path): Path of file to write input to
    """
    if day not in range(1, 26):
        raise ValueError(f"{day=} is not in range 1..25")
    while True:
        with requests.get(
            DATA_URL.substitute(year=year, day=day),
            cookies=COOKIES,
        ) as response:
            if not response.ok:
                print(Fore.RED + response.content.decode("utf-8").strip())
                sleep(1)
                continue
            response_bytes = response.content
            break
    print(
        Fore.GREEN
        + f"Got input with {len(response_bytes)} characters"
        + f" and {len(response_bytes.splitlines())} lines"
    )
    with input_path.open("wb") as input_fp:
        input_fp.write(response_bytes)


def submit_output(
    year: int,
    day: int,
    level: Literal[1, 2],
    answer: Union[str, int],
) -> str:
    """
    Upload solution to AOC website

    Args:
        year   (int)      : The year of AOC
        day    (1..25)    : The day of AOC
        level  (1, 2)     : Whether the submission is for part 1 or 2
        answer (str | int): Answer to be submitted

    Returns:
        (str): Success/failure string, with coloring
    """
    if day not in range(1, 26):
        raise ValueError(f"{day=} is not in range 1..25")
    if level not in (1, 2):
        raise ValueError(f"{level=} is not in choices (1, 2)")
    while True:
        with requests.post(
            ANSWER_URL.substitute(year=year, day=day),
            {"level": level, "answer": answer},
            cookies=COOKIES,
        ) as response:
            if not response.ok:
                sleep(1)
                continue
            html = BeautifulSoup(response.content, "html.parser")
            break
    response_text: str = html.article.p.text
    if response_text.startswith("You don't"):
        return Fore.YELLOW + response_text
    elif response_text.startswith("That's the"):
        return Fore.GREEN + response_text
    elif response_text.startswith("That's not"):
        return Fore.RED + response_text
    elif response_text.startswith("You gave"):
        return Fore.RED + response_text
    else:
        raise ValueError(f"Unknown response text: {response_text}")
