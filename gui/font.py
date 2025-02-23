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
import sys
from typing import (
    Union
)
from loguru import logger
import dearpygui.dearpygui as dpg

import utils

logger.add(**utils.log_args("gui"))


def get_font_path(font_name: str):
    try:
        font_names: list = [
            f"{str(font_name).lower()}.ttf",
            f"{str(font_name).title()}.ttf",
            f"{str(font_name).upper()}.ttf",
        ]
        lookup_dir: str = ""
        if sys.platform.startswith('win'):
            lookup_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        elif sys.platform.startswith('darwin'):
            lookup_dir = "/Library/Fonts"
        else:
            lookup_dir = "/usr/share/fonts/truetype/msttcorefonts"

        for font in font_names:
            font_path = os.path.join(lookup_dir, font)
            if os.path.exists(font_path):
                return font_path
        return None
    except Exception:
        return None


class GUIFonts:
    def font_setup(self) -> None:
        logger.debug("Setting up font")
        arial_path: str = get_font_path("arial")
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
