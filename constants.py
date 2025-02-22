import os
import tempfile

APP_NAME = "Rollover"

LOG_DIRECTORY: str = os.path.join(tempfile.gettempdir(), APP_NAME, "logs")
os.makedirs(LOG_DIRECTORY, exist_ok=True)


DEFAULT_VIEWPORT_HEIGHT: int = 700
DEFAULT_VIEWPORT_WIDTH: int = 1000

BOX_WIDTH = 400
BOX_HEIGHT = 300
MIN_WINDOW_WIDTH = BOX_WIDTH * 2 + 100

START_MAXIMIZED: bool = False

DEFAULT_FILE_DIALOG_SETTINGS: dict = {
    "directory_selector": True,
    "show": False,
    "width": 700,
    "height": 400
}
