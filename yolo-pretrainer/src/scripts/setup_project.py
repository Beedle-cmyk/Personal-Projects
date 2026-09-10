from auto_trainer import AutoTrainer
from config import (PROJECT_DIRECTORY, DATA_DIRECTORY, LABELS_JSON_FILE, LABEL_CONFIG_SEG, LABEL_CONFIG_BOX)

"""
This script generates and sets up a new Project
It will automatically extract, split and organize the data if an exported label studio .json labels file is provided

Requires:
    PROJECT_DIRECTORY
    DATA_DIRECTORY
    LABEL_CONFIG_SEG or LABEL_CONFIG_BOX

Optional (but incredibly useful):
    LABELS_JSON_FILE
"""

auto_trainer = AutoTrainer(proj_dir=PROJECT_DIRECTORY, data_dir=DATA_DIRECTORY)
auto_trainer.setup_project(label_json=LABELS_JSON_FILE, label_config=LABEL_CONFIG_SEG)