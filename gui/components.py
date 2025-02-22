from types import ModuleType
import dearpygui.dearpygui as dpg
import pathlib
from typing import (
    Callable,
    List,
    Optional,
    TYPE_CHECKING
)
import gui.structures as s
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


class FileSettingsInput:
    def __init__(
        self,
        refresh_callback: Callable,
        registry: 'Registry'
    ) -> None:
        self.refresh_callback: Callable = refresh_callback
        self.registry: 'Registry' = registry

    def refresh(self) -> None:
        logger.debug("Refreshing inp0uts")
        self.registry.use_year = dpg.get_value("use_year_checkbox") if (
            dpg.does_item_exist("use_year_checkbox")
        ) else False
        self.registry.use_suffix = dpg.get_value("use_suffix_checkbox") if (
            dpg.does_item_exist("use_suffix_checkbox")
        ) else False

        logger.debug(f"year refreshed: {self.registry.selected_year}")
        if dpg.does_item_exist("year_input"):
            self.registry.selected_year = dpg.get_value("year_input")
        if dpg.does_item_exist("suffix_input"):
            self.registry.selected_suffix = dpg.get_value("suffix_input")

    def reset(self) -> None:
        if dpg.does_item_exist("use_year_checkbox"):
            dpg.set_value("use_year_checkbox", True)
        if dpg.does_item_exist("use_suffix_checkbox"):
            dpg.set_value("use_suffix_checkbox", False)
        if dpg.does_item_exist("year_input"):
            dpg.set_value("year_input", str(utils.get_current_year()))
        if dpg.does_item_exist("suffix_input"):
            dpg.set_value("suffix_input", "")

    def layout(self) -> None:
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                id="use_year_checkbox",
                callback=self.refresh_callback,
                default_value=True
            )
            dpg.add_text("Year to replace with")
            dpg.add_combo(
                utils.get_year_range(),
                default_value=str(utils.get_current_year()),
                width=80,
                tag="year_input"
            )
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                id="use_suffix_checkbox",
                callback=self.refresh_callback,
                default_value=False
            )
            dpg.add_text("Suffix to add on the file")
            dpg.add_input_text(
                tag="suffix_input",
                width=c.BOX_WIDTH * 0.5
            )
