import os
import pathlib
from dataclasses import dataclass

from typing import (
    Union,
    Optional,
    List,
    Callable,
    Dict
)
import dearpygui.dearpygui as dpg
from loguru import logger

import gui.components as comp
import constants as c
import utils

logger.add(**utils.log_args("gui_app"))


@dataclass
class Registry:
    input_folder_root: Optional[str] = None
    output_folder_root: Optional[str] = None
    selected_files: Dict[str, bool] = None

    def __post_init__(self):
        if self.selected_files is None:
            self.selected_files = {}


class GUI:
    def __init__(self):
        logger.debug("Starting a new GUI...")
        dpg.create_context()

        self.registry: Registry = Registry()
        self._is_refreshing = False

        self.__font_setup()
        self.__layout()
        self.reset()
        self.__run()

    def reset(self):
        self.registry.input_folder_root = None
        self.registry.output_folder_root = None
        self.registry.selected_files = {}
        if dpg.does_item_exist("preview_checkbox"):
            dpg.set_value("preview_checkbox", False)
        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Rename", enabled=True)
        self.refresh()

    def refresh(self):
        if self._is_refreshing:  # Prevent recursive calls
            return

        try:
            self._is_refreshing = True
            logger.debug("Refreshing...")

            preview_enabled = dpg.get_value("preview_checkbox") if dpg.does_item_exist("preview_checkbox") else False

            # Clear existing checkboxes
            if dpg.does_item_exist("files_checkbox_group"):
                dpg.delete_item("files_checkbox_group")

            with dpg.child_window(height=250, width=c.BOX_WIDTH, tag="files_checkbox_group", parent="from_group"):
                if self.registry.input_folder_root is not None:
                    input_path = pathlib.Path(self.registry.input_folder_root)
                    files = [item for item in input_path.iterdir() if item.is_file()]

                    files.sort(key=lambda x: (0 if x.suffix.lower() == '.xlsx' else 1, x.name))

                    for file in files:
                        file_name = file.name
                        is_excel = file.suffix.lower() == '.xlsx'

                        if file_name not in self.registry.selected_files:
                            self.registry.selected_files[file_name] = is_excel

                        display_name = file_name
                        if preview_enabled:
                            name, ext = os.path.splitext(file_name)
                            display_name = f"{file_name}\n>>> {name}s{ext}"

                        dpg.add_checkbox(
                            label=display_name,
                            default_value=self.registry.selected_files[file_name],
                            callback=self.on_file_selected,
                            user_data=file_name,
                            indent=10
                        )

            if dpg.does_item_exist("to_listbox"):
                items = []
                if self.registry.output_folder_root is not None:
                    output_path = pathlib.Path(self.registry.output_folder_root)
                    items = [item.name for item in output_path.iterdir() if item.is_file()]
                dpg.configure_item("to_listbox", items=items if items else [])

            if dpg.does_item_exist("input_folder_root_preview"):
                dpg.configure_item(
                    "input_folder_root_preview",
                    default_value=self.registry.input_folder_root or ""
                )

            if dpg.does_item_exist("output_folder_root_preview"):
                dpg.configure_item(
                    "output_folder_root_preview",
                    default_value=self.registry.output_folder_root or ""
                )

        except Exception as e:
            logger.error(f"Error in refresh: {e}")
        finally:
            self._is_refreshing = False

    def on_file_selected(self, sender, app_data, user_data):
        self.registry.selected_files[user_data] = app_data
        logger.debug(f"File selection changed: {user_data} -> {app_data}")

    def on_preview_toggle(self, sender, app_data):
        self.refresh()

    def on_rename_clicked(self):
        if dpg.does_item_exist("feedback_text"):
            dpg.set_value("feedback_text", "")
            dpg.configure_item("feedback_text", color=(255, 0, 0))  # Reset to red for errors

        if not self.registry.input_folder_root:
            dpg.set_value("feedback_text", "Error: Input folder not selected")
            return

        if not self.registry.output_folder_root:
            dpg.set_value("feedback_text", "Error: Output folder not selected")
            return

        selected_files = [f for f, selected in self.registry.selected_files.items() if selected]
        if not selected_files:
            dpg.set_value("feedback_text", "Error: No files selected for renaming")
            return

        logger.info(f"Files selected for renaming: {selected_files}")
        logger.info(f"Input folder: {self.registry.input_folder_root}")
        logger.info(f"Output folder: {self.registry.output_folder_root}")

        # Display success message in green
        dpg.configure_item("feedback_text", color=(0, 255, 0))  # Green color for success
        dpg.set_value("feedback_text", f"Successfully prepared {len(selected_files)} files for renaming")

        self.registry.input_folder_root = None
        self.registry.selected_files = {}
        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Success!", enabled=False)
        self.refresh()

    def __layout(self) -> None:
        with dpg.window(
            label=c.APP_NAME,
            tag="main_window",
            min_size=[c.MIN_WINDOW_WIDTH, 400]
        ):
            if self.default_font:
                dpg.bind_font(self.default_font)

            dpg.add_text("Rollover")

            with dpg.group(horizontal=True):
                dpg.add_text("Year")
                dpg.add_combo(["2024", "2025", "2026"], default_value="2025", width=80)

            with dpg.group(horizontal=True):
                # Left group (From)
                with dpg.group(width=c.BOX_WIDTH, tag="from_group"):
                    dpg.add_text("From")
                    comp.FileDialog(
                        dpg=dpg,
                        tag="input_folder_root",
                        label="",
                        registry=self.registry,
                        callback=self.refresh
                    )
                    dpg.add_text(
                        self.registry.input_folder_root or "",
                        tag="input_folder_root_preview",
                        wrap=c.BOX_WIDTH
                    )
                    # Placeholder for checkboxes (will be populated in refresh)
                    # The empty frame will be visible even when no files are selected
                    dpg.add_child_window(height=250, width=c.BOX_WIDTH, tag="files_checkbox_group")

                # Arrow
                with dpg.group(width=50):
                    dpg.add_spacer(height=150)
                    dpg.add_text("  >>>  ")

                # Right group (To)
                with dpg.group(width=c.BOX_WIDTH):
                    dpg.add_text("To")
                    comp.FileDialog(
                        dpg=dpg,
                        tag="output_folder_root",
                        label="",
                        registry=self.registry,
                        callback=self.refresh
                    )
                    dpg.add_text(
                        self.registry.output_folder_root or "",
                        tag="output_folder_root_preview",
                        wrap=c.BOX_WIDTH
                    )
                    # Keep the normal listbox for the output side
                    dpg.add_listbox(
                        [],
                        tag="to_listbox",
                        width=c.BOX_WIDTH,
                        num_items=11
                    )

            dpg.add_checkbox(
                label="preview",
                id="preview_checkbox",
                callback=self.on_preview_toggle
            )

            dpg.add_text(
                "",
                tag="feedback_text",
                color=(255, 0, 0),
                wrap=780
            )

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

    def __run(self):
        logger.debug("Kick starting GUI!")
        dpg.setup_dearpygui()
        dpg.show_viewport()
        if c.START_MAXIMIZED:
            dpg.maximize_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def __font_setup(self) -> None:
        logger.debug("Setting up font")
        arial_path: str = utils.get_font_path("arial")
        with dpg.font_registry():
            try:
                self.default_font: Union[int, str] = dpg.add_font(arial_path, size=18)
            except Exception:
                logger.warning(f"Failed to load Arial font from {arial_path}. Using default font.")
                self.default_font: Union[int, str] = None
        logger.debug(f"OS has {arial_path} installed")
