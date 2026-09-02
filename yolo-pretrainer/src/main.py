from prelabeler import Prelabeler
from dotenv import load_dotenv
from pathlib import Path
from ultralytics import YOLO
from auto_trainer import AutoTrainer

import os

PROJECT_DIRECTORY = r"C:\Personal-Projects\yolo-pretrainer\projects"
IMG_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\images"
OUTPUT_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\outputs"
MODEL_PATH = r"C:\Personal-Projects\yolo-pretrainer\models\YOLO\best.pt"

MIN_CONF = 0.0
MAX_CONF = 1.0

load_dotenv()
# Label studio variables
API_KEY = os.environ["API_KEY"]
LABEL_STUDIO_EXE = os.environ["LABEL_STUDIO_PATH"]
LABEL_CONFIG = r"C:\Personal-Projects\yolo-pretrainer\src\cfg\label_config.xml"
LABEL_CONFIG_RAW = Path(LABEL_CONFIG).read_text(encoding="utf-8")


def main():
    autotrain()

def autotrain():

    auto_trainer = AutoTrainer(
        proj_dir=PROJECT_DIRECTORY,
        data_dir=r"C:\yolo\yolo26_v2.1_seg_234\dat\images",
    )

    # #STEP 1 - SETUP PROJECT
    auto_trainer.setup_project(
        label_json=r"C:\yolo\yolo26_v2.1_seg_234\dat\brush.json",
        label_config=LABEL_CONFIG
    )

    # STEP 2 - TRAIN MODEL
    auto_trainer.default_train()

    # STEP 3 - PRELABEL
    #auto_trainer.current_proj_dir = r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234"
    auto_trainer.default_prelabel(
        model_path=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234\runs\train\weights\best.pt",
        min_conf=0.0,
        max_conf=1.0,
        image_dir=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234\original_data\images",
        )


    #auto_trainer.studio_launch(ls_path=ls_path, api_key=api_key)

def prelabel():
    prelabeler = Prelabeler(
    MODEL_PATH,
    MIN_CONF,
    MAX_CONF,
    IMG_DIR,
    OUTPUT_DIR
    )

    prelabeler.seg_predict()

    # prelabeler.seg_predict(
    #     conf_threshold=0.5,
    #     overlap_threshold=0.7,
    #     check_duplicates=True
    # )

if __name__ == "__main__":
    main()