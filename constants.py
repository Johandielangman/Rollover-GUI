import os
import tempfile

APP_NAME = "Rollover"

LOG_DIRECTORY: str = os.path.join(tempfile.gettempdir(), APP_NAME, "logs")
os.makedirs(LOG_DIRECTORY, exist_ok=True)


DEFAULT_VIEWPORT_HEIGHT: int = 785
DEFAULT_VIEWPORT_WIDTH: int = 1000

BOX_WIDTH: int = 450
BOX_HEIGHT: int = 300
MIN_WINDOW_WIDTH: int = BOX_WIDTH * 2 + 100
SPACER_HEIGHT: int = 8
BOLD_WEIGHT: int = 700

START_MAXIMIZED: bool = False

DEFAULT_FILE_DIALOG_SETTINGS: dict = {
    "directory_selector": True,
    "show": False,
    "width": 700,
    "height": 400
}
