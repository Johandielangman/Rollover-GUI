import shutil
import os
import re
import pathlib
import datetime
from typing import (
    TYPE_CHECKING,
)
if TYPE_CHECKING:
    from gui.structures import Registry


class Rename:
    year_tolerance: int = 20

    def __init__(self, registry: 'Registry') -> None:
        self.registry: 'Registry' = registry
        self.get_year_tolerance()
        self.loop()

    def get_year_tolerance(self) -> None:
        current_year: int = datetime.date.today().year
        self.year_lower = current_year - self.year_tolerance
        self.year_upper = current_year + self.year_tolerance

    def rename_year(self, name: str) -> str:
        search: str = re.findall(r"\d{4}", name)
        if len(search) == 1:
            proposed_year = int(search[0])
            if self.year_lower <= proposed_year <= self.year_upper:
                return name.replace(str(proposed_year), self.registry.selected_year)
        elif len(search) > 1:
            search = [int(i) for i in search if self.year_lower <= int(i) <= self.year_upper]
            for year in search:
                name = name.replace(str(year), "")
        return self.add_suffix(name, f" ({self.registry.selected_year})")

    def add_suffix(
        self,
        path: str,
        suffix: str
    ) -> str:
        path = pathlib.Path(path)
        return path.stem + suffix + path.suffix

    def loop(self) -> None:
        output_root_path = pathlib.Path(self.registry.output_folder_root)
        for file in [k for k, v in self.registry.selected_files.items() if v]:
            proposed_name: str = file
            if self.registry.use_year:
                proposed_name: str = self.rename_year(file)
            if self.registry.use_suffix:
                proposed_name: str = self.add_suffix(proposed_name, self.registry.selected_suffix)
            proposed_path: pathlib.Path = output_root_path / proposed_name
            if not proposed_path.exists():
                self.registry.rename_mapping[file] = str(proposed_path.name)
            else:
                continue


def apply_rename_to_registry(registry: 'Registry') -> None:
    for from_name, to_name in registry.rename_mapping.items():
        shutil.copy(
            os.path.join(registry.input_folder_root, from_name),
            os.path.join(registry.output_folder_root, to_name)
        )
