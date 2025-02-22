from typing import (
    Union
)
import utils
from loguru import logger
import dearpygui.dearpygui as dpg

logger.add(**utils.log_args("gui"))


class GUIFonts:
    def font_setup(self) -> None:
        logger.debug("Setting up font")
        arial_path: str = utils.get_font_path("arial")
        with dpg.font_registry():
            try:
                self.default_font: Union[int, str] = dpg.add_font(arial_path, size=18)
                self.h1_font: Union[int, str] = dpg.add_font(arial_path, size=24)
                self.h2_font: Union[int, str] = dpg.add_font(arial_path, size=20)
            except Exception:
                logger.warning(f"Failed to load Arial font from {arial_path}. Using default font.")
                self.default_font: Union[int, str] = None
        logger.debug(f"OS has {arial_path} installed")

    def h1(self, text: str, **kwargs):
        dpg.bind_item_font(
            dpg.add_text(
                text,
                **kwargs
            ),
            self.h1_font
        )

    def h2(self, text: str, **kwargs):
        dpg.bind_item_font(
            dpg.add_text(
                text,
                **kwargs
            ),
            self.h2_font
        )

    def bind_default_font(self):
        if self.default_font:
            dpg.bind_font(self.default_font)
