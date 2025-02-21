import sys
import os


def get_font_path(font_name: str):
    try:
        font_names: list = [
            f"{str(font_name).lower()}.ttf",
            f"{str(font_name).title()}.ttf",
            f"{str(font_name).upper()}.ttf",
        ]
        lookup_dir: str = ""
        if sys.platform.startswith('win'):
            lookup_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        elif sys.platform.startswith('darwin'):
            lookup_dir = "/Library/Fonts"
        else:
            lookup_dir = "/usr/share/fonts/truetype/msttcorefonts"

        for font in font_names:
            font_path = os.path.join(lookup_dir, font)
            if os.path.exists(font_path):
                return font_path
        return None
    except Exception:
        return None
