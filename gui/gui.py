import os
import pathlib


from typing import (
    Union,
    Tuple,
    Optional,
    List,
    Callable,
    Dict
)
import dearpygui.dearpygui as dpg
from loguru import logger

from gui.utils import GUIUtils
from gui.font import GUIFonts
import gui.structures as s
import gui.components as comp
import constants as c
import utils

logger.add(**utils.log_args("gui_app"))


class GUI(GUIFonts, GUIUtils):
    def __init__(self):
        logger.debug("Starting a new GUI...")
        dpg.create_context()

        self.registry: s.Registry = s.Registry()
        self._is_refreshing = False

        self.__init_components()

        self.layout()
        self.reset()
        self.run()

    def __init_components(self) -> None:
        self.file_settings_input: comp.FileSettingsInput = comp.FileSettingsInput(
            refresh_callback=self.refresh,
            registry=self.registry
        )
        self.input_folder: comp.InputFolder = comp.InputFolder(
            refresh_callback=self.refresh,
            registry=self.registry
        )
        self.output_folder: comp.OutputFolder = comp.OutputFolder(
            refresh_callback=self.refresh,
            registry=self.registry
        )
        self.feedback: comp.Feedback = comp.Feedback()
        self.font_setup()

    def _reset_registry(self) -> None:
        self.registry.input_folder_root = None
        self.registry.output_folder_root = None
        self.registry.selected_files = {}

    def reset(self):
        logger.debug("Resetting...")
        self._reset_registry()

        self.file_settings_input.reset()
        self.feedback.reset()

        if dpg.does_item_exist("preview_checkbox"):
            dpg.set_value("preview_checkbox", False)

        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Rename", enabled=True)

        if (
            dpg.does_item_exist("input_folder_root_preview")
        ):
            dpg.configure_item(
                "input_folder_root_preview",
                default_value=">",
                color=s.Colors.corn_blue
            )

        if (
            dpg.does_item_exist("output_folder_root_preview")
        ):
            dpg.configure_item(
                "output_folder_root_preview",
                default_value=">",
                color=s.Colors.corn_blue
            )

        self.refresh()

    def refresh(self):
        if self._is_refreshing:  # Prevent recursive calls
            return

        try:
            self._is_refreshing = True
            logger.debug("Refreshing...")

            self.file_settings_input.refresh()

            preview_enabled = dpg.get_value("preview_checkbox") if (
                dpg.does_item_exist("preview_checkbox")
            ) else False

            # Clear existing checkboxes
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
                            preview_enabled and
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

            if dpg.does_item_exist("to_listbox"):
                items = []
                if self.registry.output_folder_root is not None:
                    output_path = pathlib.Path(self.registry.output_folder_root)
                    items = [item.name for item in output_path.iterdir() if item.is_file()]
                dpg.configure_item("to_listbox", items=items if items else [])

            if (
                dpg.does_item_exist("input_folder_root_preview") and
                self.registry.input_folder_root is not None
            ):
                dpg.configure_item(
                    "input_folder_root_preview",
                    default_value=utils.format_path_display(self.registry.input_folder_root),
                    color=s.Colors.grey
                )

            if (
                dpg.does_item_exist("output_folder_root_preview") and
                self.registry.output_folder_root is not None
            ):
                dpg.configure_item(
                    "output_folder_root_preview",
                    default_value=utils.format_path_display(self.registry.output_folder_root),
                    color=s.Colors.grey
                )

            same_folder_feedback: str = "I see you selected the input and output folder as the same folder. Is this correct?"
            if (
                self.registry.input_folder_root is not None and
                self.registry.output_folder_root is not None and
                self.registry.input_folder_root == self.registry.output_folder_root
            ):
                self.feedback.warning(same_folder_feedback)
            elif self.feedback.current_feedback == same_folder_feedback:
                self.feedback.reset()

            self.print_registry()

        except Exception as e:
            logger.error(f"Error in refresh: {e}")
        finally:
            self._is_refreshing = False

    def on_file_selected(self, sender, app_data, user_data):
        self.registry.selected_files[user_data] = app_data
        logger.debug(f"File selection changed: {user_data} -> {app_data}")

    def on_rename_clicked(self):
        self.feedback.reset()

        if not self.registry.input_folder_root:
            self.feedback.error("You need to select an input folder")
            return

        if not self.registry.output_folder_root:
            self.feedback.error("You need to select an output folder")
            return

        selected_files = [f for f, selected in self.registry.selected_files.items() if selected]
        if not selected_files:
            self.feedback.error("No files are selected for renaming")
            return

        self.print_registry()

        self.feedback.success(f"Successfully prepared {len(selected_files)} files for renaming")

        self.registry.input_folder_root = None
        self.registry.selected_files = {}
        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Success!", enabled=False)
        self.refresh()

    def layout(self) -> None:
        with dpg.window(
            label=c.APP_NAME,
            tag="main_window",
            min_size=[c.MIN_WINDOW_WIDTH, 400]
        ):
            self.bind_default_font()

            self.h1(c.APP_NAME, color=s.Colors.nice_red)

            self.add_fancy_separator()

            self.h2(
                "Choose how to rename the files",
                color=s.Colors.nice_blue
            )
            self.add_space()
            self.file_settings_input.layout()

            self.add_fancy_separator()

            self.h2(
                "Choose where to rename the files and where to save",
                color=s.Colors.nice_blue
            )
            self.add_space()

            with dpg.group(horizontal=True):
                self.input_folder.layout()

                with dpg.group(width=50):
                    dpg.add_spacer(height=150)
                    dpg.add_text("  >>>  ")

                self.output_folder.layout()

            self.feedback.layout()

            # Right-aligned buttons
            with dpg.group(horizontal=True):
                left_margin = c.BOX_WIDTH - 85
                dpg.add_spacer(width=left_margin)
                dpg.add_button(
                    label="Reset",
                    callback=self.reset,
                    width=100
                )
                dpg.add_button(
                    label="Rename",
                    callback=self.on_rename_clicked,
                    width=100,
                    tag="rename_button"
                )

        dpg.create_viewport(
            title=c.APP_NAME,
            width=c.DEFAULT_VIEWPORT_WIDTH,
            height=c.DEFAULT_VIEWPORT_HEIGHT
        )

    def run(self):
        logger.debug("Kick starting GUI!")
        dpg.setup_dearpygui()
        dpg.show_viewport()
        if c.START_MAXIMIZED:
            dpg.maximize_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
