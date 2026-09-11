from src.label_studio_manager import LabelStudioManager
from src.config import (LABEL_STUDIO_EXE, DATA_DIRECTORY)

"""
Simply launches label studio 
API will fail here as intended

Requires:
    LABEL_STUDIO_EXE

Optional:
    DATA_DIRECTORY
"""
lsManager = LabelStudioManager(api_key= None, data_dir= str(DATA_DIRECTORY), ls_path=LABEL_STUDIO_EXE, launch=True)