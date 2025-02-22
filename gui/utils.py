
from loguru import logger
import dearpygui.dearpygui as dpg
import constants as c
import utils
from typing import (
    TYPE_CHECKING
)
if TYPE_CHECKING:
    from gui.structures import Registry


logger.add(**utils.log_args("gui_app"))


class GUIUtils:
    registry: 'Registry'

    def add_space(self):
        dpg.add_spacer(height=c.SPACER_HEIGHT)

    def add_fancy_separator(self):
        self.add_space()
        dpg.add_separator()
        self.add_space()

    def print_registry(self, level: str = "info"):
        log_func = getattr(logger, level, logger.info)
        log_func(f"Files selected for renaming: {self.registry.selected_files}")
        log_func(f"Input folder: {self.registry.input_folder_root}")
        log_func(f"Output folder: {self.registry.output_folder_root}")
        log_func(f"Year Enabled: {self.registry.use_year}")
        log_func(f"Suffix Enabled: {self.registry.use_suffix}")
        log_func(f"Suffix Selected: {self.registry.selected_suffix}")
        log_func(f"Year Selected: {self.registry.selected_year}")
