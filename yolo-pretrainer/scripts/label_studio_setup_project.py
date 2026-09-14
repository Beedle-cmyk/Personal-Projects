from src.label_studio_manager import LabelStudioManager
from src.config import (API_KEY, LABEL_CONFIG_RAW, DATA_DIRECTORY, LABEL_STUDIO_EXE, LABELS_JSON_FILE)

"""
## You must ensure an instance of label studio is running! ##

Sets up a new project in label studio with the provided labelling interface, data directory & optionally labels json file
Make sure to setup local storage as per README.md guide

Requires:
    API_KEY
    LABEL_CONFIG
    DATA_DIRECTORY
    LABEL_STUDIO_EXE

Optional:
    LABELS_JSON_FILE
"""

lsManager = LabelStudioManager(api_key=API_KEY, data_dir=DATA_DIRECTORY, ls_path=LABEL_STUDIO_EXE, launch=False)
title = str(input("Enter Project Title: "))
lsManager.create_project(title=title, label_config=LABEL_CONFIG_RAW)

if LABELS_JSON_FILE is None:
    print("No JSON file provided\n")
    print("Skipping import...\n")
else:
    lsManager.import_json(project_id=lsManager.project_id, json_path=LABELS_JSON_FILE)

print(f"Project {title} successfully created!")