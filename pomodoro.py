#!python3
import sys
import argparse
import configparser
import asyncio
from pathlib import Path
from itertools import product

CONFIG_PATHS = [
    root / path for root, path in product(
        (Path("~").expanduser().absolute(), Path(".").absolute()),
        (".pomodoro", "pomodoro.ini", "pomodoro.cfg")
    )
]
OUT = sys.stdout


def get_config(args: argparse.Namespace) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    paths = [path for path in CONFIG_PATHS if path.exists()]
    defaults = {
        "short": 5,
        "long": 15,
        "work": 25
    }

    if paths:
        cfg.read(paths[0])
        cfg = cfg.get("pomodoro", {})
        if not cfg:
            cfg = defaults
    else:
        cfg["pomodoro"] = defaults
        with Path("./.pomodoro").absolute().open("w") as config:
            cfg.write(config)
        cfg = cfg["pomodoro"]

    cfg["short"] = args.short or cfg.get("short") or defaults["short"]
    cfg["long"] = args.long or cfg.get("long") or defaults["long"]
    cfg["work"] = args.work or cfg.get("work") or defaults["work"]

    return cfg


async def timer(name: str, minutes: int) -> None:
    name = name.capitalize().rjust(5)
    OUT.write(f"\r             ")
    OUT.flush()
    OUT.write(f"\r{name} {minutes:02d}:00")
    OUT.flush()

    for min in range(minutes-1, -1, -1):
        for sec in range(59, -1, -1):
            OUT.write(f"\r{name} {min:02d}:{sec:02d}")
            await asyncio.sleep(1)
            OUT.flush()

    OUT.write(f" Done.\a")
    OUT.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "initial",
        type=str,
        default="work",
        choices=["short", "long", "work"],
        help="Period to wait"
    )
    parser.add_argument("-w", "--work", type=int)
    parser.add_argument("-s", "--short", type=int)
    parser.add_argument("-l", "--long", type=int)
    args = parser.parse_args()

    cfg = get_config(args)
    asyncio.run(timer(args.initial, cfg.get(args.initial)))
