# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: February 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


import os
import pathlib
import datetime
from typing import (
    Dict,
    Optional
)

import constants as c


def get_today() -> str:
    return datetime.date.today().strftime("%Y_%m_%d")


def log_args(name: str) -> Dict:
    return {
        "sink": os.path.join(c.LOG_DIRECTORY, f"{name}_{get_today()}_.log"),
        "rotation": "1 day",
        "level": "INFO"
    }


def get_current_year() -> int:
    return datetime.date.today().year


def get_year_range() -> list:
    return [get_current_year() - 5 + i for i in range(10)]


def format_path_display(path_str: Optional[str]) -> str:
    if not path_str:
        return "No folder selected"
    try:
        path = pathlib.Path(path_str)
        parts = list(path.parts)
        if len(parts) <= 4:
            return str(path)
        return str(pathlib.Path(parts[0]) / "..." / parts[-3] / parts[-2] / parts[-1])
    except Exception:
        return "Invalid path"
