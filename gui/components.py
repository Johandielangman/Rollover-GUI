from types import ModuleType
import dearpygui.dearpygui as dpg
import pathlib
from typing import (
    Callable,
    List,
    Optional,
    TYPE_CHECKING
)
import constants as c
from loguru import logger
import utils
if TYPE_CHECKING:
    from gui.gui import Registry

logger.add(**utils.log_args("gui"))


class FileDialog:
    def __init__(
        self,
        tag: str,
        registry: 'Registry',
        callback: Optional[Callable] = None,
        label: str = ""
    ):
        self.tag: str = tag
        self.registry: 'Registry' = registry
        self.label: str = label
        self.callback: Optional[Callable] = callback
        self.__setup()

    def __setup(self) -> None:
        with dpg.group(horizontal=True):
            if self.label:
                dpg.add_text(self.label)
            dpg.add_button(
                label="Browse Folders",
                callback=lambda: dpg.show_item(self.tag)
            )

        with dpg.file_dialog(
            **c.DEFAULT_FILE_DIALOG_SETTINGS,
            callback=self.populate,
            tag=self.tag
        ):
            dpg.add_file_extension("")

    def populate(
        self,
        sender: str,
        app_data: dict
    ):
        logger.debug(app_data)
        setattr(self.registry, self.tag, app_data['file_path_name'])
        if self.callback is not None:
            self.callback()
