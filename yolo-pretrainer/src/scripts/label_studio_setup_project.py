from label_studio_manager import LabelStudioManager
from config import (API_KEY, LABEL_CONFIG_SEG, DATA_DIRECTORY, LABEL_STUDIO_EXE, LABELS_JSON_FILE)

"""
Sets up a new project in label studio with the provided labelling interface, data directory & optionally labels json file
Make sure to setup local storage as per README.md guide

Requires:
    API_KEY
    LABEL_CONFIG_SEG
    DATA_DIRECTORY
    LABEL_STUDIO_EXE

Optional:
    LABELS_JSON_FILE
"""

lsManager = LabelStudioManager(api_key=API_KEY, data_dir=DATA_DIRECTORY, ls_path=LABEL_STUDIO_EXE, launch=False)
title = str(input("Enter Project Title: "))
lsManager.create_project(title=title, label_config=LABEL_CONFIG_SEG)
lsManager.import_json(project_id=lsManager.project_id, json_path=LABELS_JSON_FILE)