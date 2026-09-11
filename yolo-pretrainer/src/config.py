"""
Central configuration for the src classes.

Edit the paths below (or set the matching environment variables) to point
at your actual source files
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------- Directory paths ---------------------------------------------------------- #
# PLEASE FILL THIS IN
BASE_DIRECTORY = Path(r"FILL THIS IN!")  # Where your repository is e.g. C:/borescope-yolo-training

PROJECT_DIRECTORY = BASE_DIRECTORY / r"projects"
DATA_DIRECTORY = BASE_DIRECTORY / r"data/images"
CFG_DIRECTORY = BASE_DIRECTORY / r"src/cfg"

# Provide a label studio exported json file e.g. yolo26_v2.1_seg_234.json
LABELS_JSON_FILE = r"FILL THIS IN!"

# Create a project using setup_project.py first before setting this
CURRENT_WORKING_PROJECT_DIRECTORY = PROJECT_DIRECTORY / r"FILL THIS IN!"  #e.g. yolo26_v1.2_seg_2808
# ---------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------- environ (private data) ---------------------------------------------------------- #
API_KEY = os.environ["API_KEY"]
LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]
# ----------------------------------------------------------------------------------------------------------------------------- #



# --------------------------Labelling Interface Templates (Copy-pasted from label studio) --------------------- #
#LABEL_CONFIG_BOX = CFG_DIRECTORY / r"label_config_box.xml"
LABEL_CONFIG_SEG = CFG_DIRECTORY / r"label_config_seg.xml"

# SET LABEL_CONFIG for either segmentation or box; Default is segmentation
LABEL_CONFIG = LABEL_CONFIG_SEG
LABEL_CONFIG_RAW = Path(LABEL_CONFIG).read_text(encoding="utf-8")
# ------------------------------------------------------------------------------------------------------------- #



# --------------------------------------Training Args Configs-------------------------------------------------- #
ARGS_YAML_CONFIG = CURRENT_WORKING_PROJECT_DIRECTORY /  r"cfg/args.yaml"
TUNE_ARGS_YAML_CONFIG = CURRENT_WORKING_PROJECT_DIRECTORY / r"cfg/tune_args.yaml"

# Enabling this will auto write the tuner recommended parameters from 'best_hyperparameters.yaml' to the current project's 'args.yaml' in tune.py
UPDATE_ARGS_YAML_WITH_TUNED_ONES = False

# Path to model if you would like to resume training from a checkpoint e.g. "project/runs/last.pt"
RESUME_MODEL = None

# trainer.py maximum amount of times training attempts to resume
MAX_RETRIES = 3
# ------------------------------------------------------------------------------------------------------------- #



# --------------------------------------Prediction/Prelabelling Args Configs-------------------------------------------------- #
# Model path e.g. to best.pt used for predictions or prelabelling
MODEL_FOR_PREDICTIONS = r"FILL THIS IN!"
MIN_CONF = 0.25
MAX_CONF = 1.0
IMAGES_TO_PREDICT = r"FILL THIS IN!"
# ---------------------------------------------------------------------------------------------------------------------------- #