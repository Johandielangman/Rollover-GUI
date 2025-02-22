from types import ModuleType
import dearpygui.dearpygui as dpg
import pathlib
import os
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


class InputFolder:
    def __init__(
        self,
        refresh_callback: Callable,
        registry: 'Registry'
    ) -> None:
        self.refresh_callback: Callable = refresh_callback
        self.registry: 'Registry' = registry

    @property
    def preview_enabled(self) -> bool:
        return dpg.get_value("preview_checkbox") if (
            dpg.does_item_exist("preview_checkbox")
        ) else False

    def on_file_selected(self, sender, app_data, user_data):
        self.registry.selected_files[user_data] = app_data
        logger.debug(f"File selection changed: {user_data} -> {app_data}")

    def refresh(self) -> None:
        if dpg.does_item_exist("files_checkbox_group"):
            dpg.delete_item("files_checkbox_group")

        with dpg.child_window(
            height=c.BOX_HEIGHT,
            width=c.BOX_WIDTH,
            tag="files_checkbox_group",
            parent="from_group",
            horizontal_scrollbar=True
        ):
            if self.registry.input_folder_root is not None:
                input_path = pathlib.Path(self.registry.input_folder_root)
                files = [item for item in input_path.iterdir() if item.is_file()]

                files.sort(
                    key=lambda x: (
                        0 if
                        x.suffix.lower() == '.xlsx'
                        else 1, x.name
                    )
                )

                for file in files:
                    is_excel = file.suffix.lower() == '.xlsx'

                    if file.name not in self.registry.selected_files:
                        self.registry.selected_files[file.name] = is_excel

                    preview_name = ""
                    if (
                        self.preview_enabled and
                        self.registry.selected_files[file.name]
                    ):
                        name, ext = os.path.splitext(file.name)
                        preview_name = f">> {name}s{ext}"

                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(
                            label=file.name,
                            default_value=self.registry.selected_files[file.name],
                            callback=self.on_file_selected,
                            user_data=file.name,
                        )
                        dpg.add_text(
                            default_value=preview_name,
                            color=s.Colors.yellow,
                        )

        if (
            dpg.does_item_exist("input_folder_root_preview") and
            self.registry.input_folder_root is not None
        ):
            dpg.configure_item(
                "input_folder_root_preview",
                default_value=utils.format_path_display(self.registry.input_folder_root),
                color=s.Colors.grey
            )

    def reset(self) -> None:
        if dpg.does_item_exist("preview_checkbox"):
            dpg.set_value("preview_checkbox", False)

        if dpg.does_item_exist("input_folder_root_preview"):
            dpg.configure_item(
                "input_folder_root_preview",
                default_value=">",
                color=s.Colors.corn_blue
            )

    def layout(self) -> None:
        with dpg.group():
            with dpg.group(width=c.BOX_WIDTH, tag="from_group"):
                dpg.add_text("Input Location")
                FileDialog(
                    tag="input_folder_root",
                    label="",
                    registry=self.registry,
                    callback=self.refresh_callback
                )
                dpg.add_text(
                    ">",
                    tag="input_folder_root_preview",
                    wrap=c.BOX_WIDTH,
                    color=s.Colors.corn_blue
                )
                dpg.add_child_window(
                    height=c.BOX_HEIGHT,
                    width=c.BOX_WIDTH,
                    tag="files_checkbox_group"
                )
            dpg.add_checkbox(
                label="Preview Update",
                id="preview_checkbox",
                callback=self.refresh_callback
            )


class OutputFolder:
    def __init__(
        self,
        refresh_callback: Callable,
        registry: 'Registry'
    ) -> None:
        self.refresh_callback: Callable = refresh_callback
        self.registry: 'Registry' = registry

    def refresh(self) -> None:
        if dpg.does_item_exist("to_listbox"):
            items = []
            if self.registry.output_folder_root is not None:
                output_path = pathlib.Path(self.registry.output_folder_root)
                items = [item.name for item in output_path.iterdir() if item.is_file()]
            dpg.configure_item("to_listbox", items=items if items else [])

        if (
            dpg.does_item_exist("output_folder_root_preview") and
            self.registry.output_folder_root is not None
        ):
            dpg.configure_item(
                "output_folder_root_preview",
                default_value=utils.format_path_display(self.registry.output_folder_root),
                color=s.Colors.grey
            )

    def reset(self) -> None:
        if dpg.does_item_exist("output_folder_root_preview"):
            dpg.configure_item(
                "output_folder_root_preview",
                default_value=">",
                color=s.Colors.corn_blue
            )

    def layout(self) -> None:
        with dpg.group(width=c.BOX_WIDTH):
            dpg.add_text("Output Location")
            FileDialog(
                tag="output_folder_root",
                label="",
                registry=self.registry,
                callback=self.refresh_callback
            )
            dpg.add_text(
                ">",
                tag="output_folder_root_preview",
                wrap=c.BOX_WIDTH,
                color=s.Colors.corn_blue
            )
            dpg.add_listbox(
                [],
                tag="to_listbox",
                width=c.BOX_WIDTH,
                num_items=c.BOX_HEIGHT // 22
            )


class Feedback:
    def __update(self, msg: str, color: tuple) -> None:
        if dpg.does_item_exist("feedback_text"):
            dpg.set_value("feedback_text", msg)
            dpg.configure_item("feedback_text", color=color)

    @property
    def current_feedback(self) -> str:
        return dpg.get_value("feedback_text")

    def info(self, msg: str) -> None:
        self.__update(msg, s.Colors.teal)

    def success(self, msg: str) -> None:
        self.__update(msg, s.Colors.green)

    def error(self, msg: str) -> None:
        self.__update(msg, s.Colors.red)

    def warning(self, msg: str) -> None:
        self.__update(msg, s.Colors.yellow)

    def reset(self) -> None:
        self.__update("", s.Colors.red)

    def layout(self) -> None:
        dpg.add_text(
            "",
            tag="feedback_text",
            color=s.Colors.red,
            wrap=c.MIN_WINDOW_WIDTH
        )
