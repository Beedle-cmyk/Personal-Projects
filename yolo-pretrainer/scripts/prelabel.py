from src.prelabeler import Prelabeler
from src.config import (MODEL_FOR_PREDICTIONS, MIN_CONF, MAX_CONF, IMAGES_TO_PREDICT, CURRENT_WORKING_PROJECT_DIRECTORY)
from pathlib import Path

"""
Generates prediction labels for the images of your choice

Requires: 
    MODEL_FOR_PREDICTIONS
    MIN_CONF
    MAX_CONF
    IMAGES_TO_PREDICT

Optional:
    CURRENT_WORKING_PROJECT_DIRECTORY
"""

if CURRENT_WORKING_PROJECT_DIRECTORY is None:
    valid = False
    while not valid:
        output_dir = str(input("Enter save Directory for labels:"))
        if Path(output_dir).exists():
            valid = True
else:
    output_dir = CURRENT_WORKING_PROJECT_DIRECTORY / r"prelabels"

prelabeler = Prelabeler(
    model_path=MODEL_FOR_PREDICTIONS, 
    min_conf=MIN_CONF, 
    max_conf=MAX_CONF, 
    image_dir=IMAGES_TO_PREDICT,
    output_dir=output_dir
)

prelabeler.seg_predict()