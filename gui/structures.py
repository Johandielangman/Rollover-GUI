from typing import (
    Optional,
    Dict
)
from pydantic import BaseModel
from dataclasses import dataclass, field


# class Registry(BaseModel):
#     input_folder_root: Optional[str] = None
#     output_folder_root: Optional[str] = None
#     selected_files: Dict[str, str] = {}

#     use_year: bool = False
#     use_suffix: bool = False

#     selected_year: str = ""
#     selected_suffix: str = ""


@dataclass
class Registry:
    input_folder_root: Optional[str] = None
    output_folder_root: Optional[str] = None
    selected_files: Dict[str, str] = field(default_factory=dict)

    use_year: bool = False
    use_suffix: bool = False

    selected_year: str = ""
    selected_suffix: str = ""


@dataclass
class Colors:
    red: tuple = (255, 0, 0)
    nice_red: tuple = (233, 79, 100)
    yellow: tuple = (255, 255, 0)
    white: tuple = (255, 255, 255)
    teal: tuple = (0, 255, 255)
    blue: tuple = (30, 144, 255)
    nice_blue: tuple = (70, 188, 222)
    green: tuple = (0, 255, 0)
    corn_blue: tuple = (100, 149, 237)
    grey: tuple = (128, 128, 128)
