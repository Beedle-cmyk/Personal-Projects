from src.label_studio_manager import LabelStudioManager
from src.config import (LABEL_STUDIO_EXE, DATA_DIRECTORY)
from pathlib import Path

"""
Simply launches label studio 
API will fail here as intended

Requires:
    LABEL_STUDIO_EXE

Optional:
    DATA_DIRECTORY
"""

data_dir = DATA_DIRECTORY.parent
lsManager = LabelStudioManager(api_key= None, data_dir= str(data_dir), ls_path=LABEL_STUDIO_EXE, launch=True)