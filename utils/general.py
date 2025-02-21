
import os
from typing import (
    Dict
)
import constants as c
import datetime


def get_today() -> str:
    return datetime.date.today().strftime("%Y_%m_%d")


def log_args(name: str) -> Dict:
    return {
        "sink": os.path.join(c.LOG_DIRECTORY, f"{name}_{get_today()}_.log"),
        "rotation": "1 day",
        "level": "INFO"
    }
