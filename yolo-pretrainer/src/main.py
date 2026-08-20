from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager
from dotenv import load_dotenv
from pathlib import Path

import os

MODEL_PATH = r"C:\Personal-Projects\yolo-pretrainer\models\YOLO\best.pt"
IMG_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\images"
OUTPUT_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\outputs"

MIN_CONF = 0.0
MAX_CONF = 1.0

load_dotenv()
api_key = os.environ["API_KEY"]
ls_path = os.environ["LABEL_STUDIO_PATH"]
label_config = Path("label_config.xml").read_text(encoding="utf-8")

def main():
    prelabel()
    #labelstudio()
    print("END")

def trainer():
    pass

def labelstudio():
    ls = LabelStudioManager(api_key=api_key, data_dir="C:\\Personal-Projects\\yolo-pretrainer\\data")
    proj_id = ls.new_project(title="TESTING", label_config=label_config)
    ls.import_json(project_id=proj_id, json_path="C:\\Personal-Projects\\yolo-pretrainer\\data\\outputs\\seg_predictions.json")

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