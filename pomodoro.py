#!python3
import sys
import argparse
import configparser
import asyncio
from pathlib import Path
from itertools import product

CONFIG_PATHS = [
    root / path
    for root, path in product(
        (Path("~").expanduser().absolute(), Path(".").absolute()),
        (".pomodoro", "pomodoro.ini", "pomodoro.cfg"),
    )
]
OUT = sys.stdout


def get_config(args: argparse.Namespace) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    paths = [path for path in CONFIG_PATHS if path.exists()]
    defaults = {"short": 5, "long": 15, "work": 25}

    if paths:
        cfg.read(paths[0])
    else:
        cfg["pomodoro"] = {}

    cfg["pomodoro"]["short"] = str(
        args.short or cfg["pomodoro"].getint("short") or defaults["short"]
    )
    cfg["pomodoro"]["long"] = str(args.long or cfg["pomodoro"].getint("long") or defaults["long"])
    cfg["pomodoro"]["work"] = str(args.work or cfg["pomodoro"].getint("work") or defaults["work"])

    return cfg


async def timer(name: str, minutes: int) -> None:
    """
    Down counting timer that rings a terminal bell after reaching 00:00.

    Args:
        name (str): Name of the period
        minutes (int): Minutes to count down
    """
    name = name.capitalize().rjust(5)
    OUT.write(f"                             \r")
    OUT.flush()

    OUT.write(f"\r{name} {minutes:02d}:00")
    OUT.flush()

    for min in range(minutes - 1, -1, -1):
        for sec in range(59, -1, -1):
            await asyncio.sleep(1)
            OUT.write(f"\r{name} {min:02d}:{sec:02d}")
            OUT.flush()

    OUT.write(" Done.")
    OUT.write("\a\n")
    OUT.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line Pomodoro timer.")
    parser.add_argument(
        "cmd", type=str, default="work", choices=["short", "long", "work"], help="Period to wait"
    )
    parser.add_argument("-w", "--work", type=int, help="Default 25 min.")
    parser.add_argument("-s", "--short", type=int, help="Default 5 min.")
    parser.add_argument("-l", "--long", type=int, help="Default 15 min.")
    args = parser.parse_args()

    cfg = get_config(args)
    try:
        minutes = cfg["pomodoro"].getint(args.cmd, 0)
        asyncio.run(timer(name=args.cmd, minutes=minutes))
    except KeyboardInterrupt:
        exit()
