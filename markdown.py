import pathlib
import os

from spire.doc import *
from spire.doc.common import *

ROOT_PATH = pathlib.Path(__file__).parent.absolute()
MARKDOWN_PATH = os.path.join(ROOT_PATH, "README.md")
DOCX_PATH = os.path.join(ROOT_PATH, "docs", "readme.docx")

document = Document()

# Load a Markdown file
document.LoadFromFile(MARKDOWN_PATH)

# Save it as a docx file
document.SaveToFile(DOCX_PATH, FileFormat.Docx2016)

# Dispose resources
document.Dispose()
