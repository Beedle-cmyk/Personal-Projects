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
BASE_DIRECTORY = Path(r"C:\Personal-Projects\yolo-pretrainer")

# Please Set this to your current working project e.g. C:\borescope-yolo-training\projects\yolo26_v1.7_seg_900
CURRENT_WORKING_PROJECT_DIRECTORY = Path(r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v2.2_seg_234")

PROJECT_DIRECTORY = BASE_DIRECTORY / r"projects"
DATA_DIRECTORY = BASE_DIRECTORY / r"data/images"
CFG_DIRECTORY = BASE_DIRECTORY / r"src/cfg"

# Provide a label
LABELS_JSON_FILE = r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v2.1_seg_234\labelstudio\yolo26_v2.1_seg_234.json"

API_KEY = os.environ["API_KEY"]
LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]

# ---- Labelling Interface Templates (Copy-pasted from label studio) ----
LABEL_CONFIG_BOX = CFG_DIRECTORY / r"label_config_box.xml"
LABEL_CONFIG_SEG = CFG_DIRECTORY / r"label_config_seg.xml"

# SET LABEL_CONFIG for either segmentation or box
LABEL_CONFIG = LABEL_CONFIG_SEG
LABEL_CONFIG_RAW = Path(LABEL_CONFIG).read_text(encoding="utf-8")

# Enabling this will auto write the tuner recommended parameters from 'best_hyperparameters.yaml' to the current project's 'args.yaml'
# This is used in tune.py
UPDATE_ARGS_YAML_WITH_TUNED_ONES = False
ARGS_YAML_CONFIG = CURRENT_WORKING_PROJECT_DIRECTORY / r"cfg/args.yaml"
TUNE_ARGS_YAML_CONFIG = CURRENT_WORKING_PROJECT_DIRECTORY / r"cfg/tune_args.yaml"

# Path to model if you would like to resume training from a checkpoint
RESUME_MODEL = None

# trainer.py maximum amount of times training attempts to resume
MAX_RETRIES = 3