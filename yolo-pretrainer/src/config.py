"""
Central configuration for the src classes.

Edit the paths below (or set the matching environment variables) to point
at your actual source files
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#BASE_DIRECTORY = Path(r"C:\borescope-yolo-training")
BASE_DIRECTORY = Path(r"C:\Personal-Projects/yolo-pretrainer")

PROJECT_DIRECTORY = BASE_DIRECTORY / r"projects"
DATA_DIRECTORY = BASE_DIRECTORY / r"data/images"

CFG_DIRECTORY = BASE_DIRECTORY / r"src/cfg"

API_KEY = os.environ["API_KEY"]

LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]

LABEL_CONFIG_BOX = CFG_DIRECTORY / r"label_config_box.xml"
LABEL_CONFIG_BOX_RAW = Path(LABEL_CONFIG_BOX).read_text(encoding="utf-8")

LABEL_CONFIG_SEG = CFG_DIRECTORY / r"label_config_seg.xml"
LABEL_CONFIG_SEG_RAW = Path(LABEL_CONFIG_SEG).read_text(encoding="utf-8")