"""
Central configuration for the src classes.

Edit the paths below (or set the matching environment variables) to point
at your actual source files
"""

import os
from pathlib import Path

BASE_DIRECTORY = Path(r"C:\borescope-yolo-training")

PROJECT_DIRECTORY = BASE_DIRECTORY / r"projects"
DATA_DIRECTORY = BASE_DIRECTORY / r"data/images"
API_KEY = os.environ["API_KEY"]

LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]
LABEL_CONFIG = BASE_DIRECTORY / r"src\cfg\label_config.xml"
LABEL_CONFIG_RAW = Path(LABEL_CONFIG).read_text(encoding="utf-8")