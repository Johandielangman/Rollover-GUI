from types import ModuleType
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
        dpg: ModuleType,
        tag: str,
        registry: 'Registry',
        callback: Optional[Callable] = None,
        label: str = ""
    ):
        self.dpg: ModuleType = dpg
        self.tag: str = tag
        self.registry: 'Registry' = registry
        self.label: str = label
        self.callback: Optional[Callable] = callback
        self.__setup()

    def __setup(self) -> None:
        with self.dpg.group(horizontal=True):
            if self.label:
                self.dpg.add_text(self.label)
            self.dpg.add_button(
                label="Browse Folders",
                callback=lambda: self.dpg.show_item(self.tag)
            )

        with self.dpg.file_dialog(
            **c.DEFAULT_FILE_DIALOG_SETTINGS,
            callback=self.populate,
            tag=self.tag
        ):
            self.dpg.add_file_extension("")

    def populate(
        self,
        sender: str,
        app_data: dict
    ):
        logger.debug(app_data)
        setattr(self.registry, self.tag, app_data['file_path_name'])
        if self.callback is not None:
            self.callback()
