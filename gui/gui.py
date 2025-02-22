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

import gui.structures as s
import gui.components as comp
import constants as c
import utils

logger.add(**utils.log_args("gui_app"))


class GUI:
    def __init__(self):
        logger.debug("Starting a new GUI...")
        dpg.create_context()

        self.registry: s.Registry = s.Registry()
        self._is_refreshing = False

        self.__font_setup()
        self.__layout()
        self.reset()
        self.__run()

    def reset(self):
        logger.debug("Resetting...")
        self.registry.input_folder_root = None
        self.registry.output_folder_root = None
        self.registry.selected_files = {}
        if dpg.does_item_exist("preview_checkbox"):
            dpg.set_value("preview_checkbox", False)
        if dpg.does_item_exist("use_year_checkbox"):
            dpg.set_value("use_year_checkbox", True)
        if dpg.does_item_exist("use_suffix_checkbox"):
            dpg.set_value("use_suffix_checkbox", False)

        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Rename", enabled=True)

        if dpg.does_item_exist("feedback_text"):
            dpg.set_value("feedback_text", "")

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

        if dpg.does_item_exist("year_input"):
            dpg.set_value("year_input", str(utils.get_current_year()))
        if dpg.does_item_exist("suffix_input"):
            dpg.set_value("suffix_input", "")
        self.refresh()

    def get_checkbox_states(self) -> Tuple[bool, bool, bool]:
        use_year_enabled = dpg.get_value("use_year_checkbox") if (
            dpg.does_item_exist("use_year_checkbox")
        ) else False
        use_suffix_enabled = dpg.get_value("use_suffix_checkbox") if (
            dpg.does_item_exist("use_suffix_checkbox")
        ) else False
        preview_enabled = dpg.get_value("preview_checkbox") if (
            dpg.does_item_exist("preview_checkbox")
        ) else False
        return (
            use_year_enabled,
            use_suffix_enabled,
            preview_enabled
        )

    def get_file_update_selections(self):
        if dpg.does_item_exist("year_input"):
            self.registry.selected_year = dpg.get_value("year_input")
        if dpg.does_item_exist("suffix_input"):
            self.registry.selected_suffix = dpg.get_value("suffix_input")

    def refresh(self):
        if self._is_refreshing:  # Prevent recursive calls
            return

        try:
            self._is_refreshing = True
            logger.debug("Refreshing...")

            (
                self.registry.use_year,
                self.registry.use_suffix,
                preview_enabled
            ) = self.get_checkbox_states()
            self.get_file_update_selections()

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

            self.print_registry()

        except Exception as e:
            logger.error(f"Error in refresh: {e}")
        finally:
            self._is_refreshing = False

    def on_file_selected(self, sender, app_data, user_data):
        self.registry.selected_files[user_data] = app_data
        logger.debug(f"File selection changed: {user_data} -> {app_data}")

    def print_registry(self, level: str = "info"):
        log_func = getattr(logger, level, logger.info)
        log_func(f"Files selected for renaming: {self.registry.selected_files}")
        log_func(f"Input folder: {self.registry.input_folder_root}")
        log_func(f"Output folder: {self.registry.output_folder_root}")
        log_func(f"Year Enabled: {self.registry.use_year}")
        log_func(f"Suffix Enabled: {self.registry.use_suffix}")
        log_func(f"Suffix Selected: {self.registry.selected_suffix}")
        log_func(f"Year Selected: {self.registry.selected_year}")

    def on_rename_clicked(self):
        if dpg.does_item_exist("feedback_text"):
            dpg.set_value("feedback_text", "")
            dpg.configure_item("feedback_text", color=s.Colors.red)  # Reset to red for errors

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

        self.print_registry()

        # Display success message in green
        dpg.configure_item("feedback_text", color=s.Colors.green)  # Green color for success
        dpg.set_value("feedback_text", f"Successfully prepared {len(selected_files)} files for renaming")

        self.registry.input_folder_root = None
        self.registry.selected_files = {}
        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Success!", enabled=False)
        self.refresh()

    def add_space(self):
        dpg.add_spacer(height=c.SPACER_HEIGHT)

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

    def __layout(self) -> None:
        with dpg.window(
            label=c.APP_NAME,
            tag="main_window",
            min_size=[c.MIN_WINDOW_WIDTH, 400]
        ):
            if self.default_font:
                dpg.bind_font(self.default_font)

            self.h1(c.APP_NAME, color=s.Colors.nice_red)

            self.add_space()
            dpg.add_separator()
            self.add_space()

            self.h2(
                "Choose how to rename the files",
                color=s.Colors.nice_blue
            )
            self.add_space()

            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    id="use_year_checkbox",
                    callback=self.refresh,
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
                    callback=self.refresh,
                    default_value=False
                )
                dpg.add_text("Suffix to add on the file")
                dpg.add_input_text(
                    tag="suffix_input",
                    width=c.BOX_WIDTH * 0.5
                )

            self.add_space()
            dpg.add_separator()
            self.add_space()

            self.h2(
                "Choose where to rename the files and where to save",
                color=s.Colors.nice_blue
            )
            self.add_space()

            with dpg.group(horizontal=True):
                # Left group (From)
                with dpg.group(width=c.BOX_WIDTH, tag="from_group"):
                    dpg.add_text("Input Location")
                    comp.FileDialog(
                        dpg=dpg,
                        tag="input_folder_root",
                        label="",
                        registry=self.registry,
                        callback=self.refresh
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

                with dpg.group(width=50):
                    dpg.add_spacer(height=150)
                    dpg.add_text("  >>>  ")

                with dpg.group(width=c.BOX_WIDTH):
                    dpg.add_text("Output Location")
                    comp.FileDialog(
                        dpg=dpg,
                        tag="output_folder_root",
                        label="",
                        registry=self.registry,
                        callback=self.refresh
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

            dpg.add_checkbox(
                label="Preview Update",
                id="preview_checkbox",
                callback=self.refresh
            )

            dpg.add_text(
                "",
                tag="feedback_text",
                color=s.Colors.red,
                wrap=c.MIN_WINDOW_WIDTH
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
                self.h1_font: Union[int, str] = dpg.add_font(arial_path, size=24)
                self.h2_font: Union[int, str] = dpg.add_font(arial_path, size=20)
            except Exception:
                logger.warning(f"Failed to load Arial font from {arial_path}. Using default font.")
                self.default_font: Union[int, str] = None
        logger.debug(f"OS has {arial_path} installed")
