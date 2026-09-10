"""
Central configuration for the src classes.

Edit the paths below (or set the matching environment variables) to point
at your actual source files
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---- Directory paths ----
#BASE_DIRECTORY = Path(r"C:\borescope-yolo-training")
BASE_DIRECTORY = Path(r"C:\Personal-Projects/yolo-pretrainer")

# Please Set this to your current working project e.g. C:\borescope-yolo-training\projects\yolo26_v1.7_seg_900
CURRENT_WORKING_PROJECT_DIRECTORY = None

PROJECT_DIRECTORY = BASE_DIRECTORY / r"projects"
DATA_DIRECTORY = BASE_DIRECTORY / r"data/images"
CFG_DIRECTORY = BASE_DIRECTORY / r"src/cfg"

# Provide a label
LABELS_JSON_FILE = None

API_KEY = os.environ["API_KEY"]
LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]

# ---- Labelling Interface Templates (Copy-pasted from label studio) ----
LABEL_CONFIG_BOX = CFG_DIRECTORY / r"label_config_box.xml"
LABEL_CONFIG_SEG = CFG_DIRECTORY / r"label_config_seg.xml"
LABEL_CONFIG_BOX_RAW = Path(LABEL_CONFIG_BOX).read_text(encoding="utf-8")
LABEL_CONFIG_SEG_RAW = Path(LABEL_CONFIG_SEG).read_text(encoding="utf-8")

# Enabling this will auto write the tuner recommended parameters from 'best_hyperparameters.yaml' to the current project's 'args.yaml'
# This is used in tune.py
UPDATE_ARGS_YAML_WITH_TUNED_ONES = False

# trainer.py maximum amount of times training attempts to resume
MAX_RETRIES = 3