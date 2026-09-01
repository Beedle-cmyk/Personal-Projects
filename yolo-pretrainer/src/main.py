from prelabeler import Prelabeler
from dotenv import load_dotenv
from pathlib import Path
from ultralytics import YOLO
from auto_trainer import AutoTrainer

import os

MODEL_PATH = r"C:\Personal-Projects\yolo-pretrainer\models\YOLO\best.pt"
IMG_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\images"
OUTPUT_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\outputs"

MIN_CONF = 0.0
MAX_CONF = 1.0

load_dotenv()
api_key = os.environ["API_KEY"]
ls_path = os.environ["LABEL_STUDIO_PATH"]
label_config = Path(r"C:\Personal-Projects\yolo-pretrainer\src\cfg\label_config.xml").read_text(encoding="utf-8")

def main():
    autotrain()


def autotrain():

    auto_trainer = AutoTrainer(
        proj_dir=r"C:\Personal-Projects\yolo-pretrainer\projects",
        data_dir=r"C:\yolo\yolo26_v2.1_seg_234\dat\images",
    )

    auto_trainer.setup_project(
        label_json=r"C:\yolo\yolo26_v2.1_seg_234\dat\brush.json",
        label_config=r"C:\Personal-Projects\yolo-pretrainer\src\cfg\label_config.xml"
    )

    #auto_trainer.default_train(args_yaml="cfg/args.yaml")
    #auto_trainer.studio_launch(ls_path=ls_path, api_key=api_key)
    



def training():
    model = YOLO("")



def trainer():
    pass



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