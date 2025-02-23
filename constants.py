# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: February 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

import os
import tempfile

# =========== // DEAR PY GUI SPECIFIC // ===========

APP_NAME = "Rollover!"

BOX_WIDTH: int = 450
BOX_HEIGHT: int = 300

DEFAULT_VIEWPORT_HEIGHT: int = 785
DEFAULT_VIEWPORT_WIDTH: int = 1000
MIN_WINDOW_WIDTH: int = BOX_WIDTH * 2 + 100

SPACER_HEIGHT: int = 8

START_MAXIMIZED: bool = False

DEFAULT_FILE_DIALOG_SETTINGS: dict = {
    "directory_selector": True,
    "show": False,
    "width": 700,
    "height": 400
}

# =========== // LOGGER DIRECTORY // ===========

LOG_DIRECTORY: str = os.path.join(tempfile.gettempdir(), APP_NAME, "logs")
os.makedirs(LOG_DIRECTORY, exist_ok=True)
