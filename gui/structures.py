from typing import (
    Optional,
    Dict
)
from dataclasses import dataclass, field


@dataclass
class Registry:
    input_folder_root: Optional[str] = None
    output_folder_root: Optional[str] = None
    selected_files: Dict = field(default_factory=dict)

    use_year: bool = False
    use_suffix: bool = False

    selected_year: str = ""
    selected_suffix: str = ""


@dataclass
class Colors:
    red: tuple = (255, 0, 0)
    yellow: tuple = (255, 255, 0)
    white: tuple = (255, 255, 255)
    teal: tuple = (0, 255, 255)
    blue: tuple = (30, 144, 255)
    green: tuple = (0, 255, 0)
