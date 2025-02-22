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
        self.registry.rename_mapping = {}

    def reset(self):
        logger.debug("Resetting...")
        self._reset_registry()

        self.file_settings_input.reset()
        self.feedback.reset()
        self.input_folder.reset()
        self.output_folder.reset()

        if dpg.does_item_exist("rename_button"):
            dpg.configure_item("rename_button", label="Rename", enabled=True)

        self.refresh()

    def validate_folder_choices(self) -> None:
        same_folder_feedback: str = "I see you selected the input and output folder as the same folder. Is this correct?"
        if (
            self.registry.input_folder_root is not None and
            self.registry.output_folder_root is not None and
            self.registry.input_folder_root == self.registry.output_folder_root
        ):
            self.feedback.warning(same_folder_feedback)
        elif self.feedback.current_feedback == same_folder_feedback:
            self.feedback.reset()

    def refresh(self):
        if self._is_refreshing:  # Prevent recursive calls
            return

        try:
            self._is_refreshing = True
            logger.debug("Refreshing...")

            self.file_settings_input.refresh()
            self.input_folder.refresh()
            self.output_folder.refresh()

            self.validate_folder_choices()

            self.print_registry()
        except Exception as e:
            logger.error(f"Error in refresh: {e}")
        finally:
            self._is_refreshing = False

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
        utils.Rename(
            registry=self.registry
        )
        if not self.registry.rename_mapping:
            self.feedback.error("Nothing to rename!")
            return

        utils.apply_rename_to_registry(self.registry)

        self.feedback.success(f"Successfully renamed {len(self.registry.rename_mapping)} file(s). Please reset to rename more files.")

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
            dpg.add_text("Your one stop shop to rename a bunch of files in bulk!")

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
                    dpg.add_spacer(height=175)
                    dpg.add_text("  >>>  ")

                self.output_folder.layout()

            self.feedback.layout()

            # Right-aligned buttons
            with dpg.group(horizontal=True):
                left_margin = c.BOX_WIDTH - 80
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
