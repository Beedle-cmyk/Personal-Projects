from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager
from dotenv import load_dotenv
import os

MODEL_PATH = r"C:\Personal-Projects\yolo-pretrainer\models\YOLO\best.pt"
IMG_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\images"
OUTPUT_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\outputs"

MIN_CONF = 0.0
MAX_CONF = 1.0

load_dotenv()
api_key = os.environ["API_KEY"]
ls_path = os.environ["LABEL_STUDIO_PATH"]

def main():
    labelstudio()


def labelstudio():

    print(api_key)
    ls = LabelStudioManager(
        ls_path=ls_path,
        data_dir="C:\\Personal-Projects\\yolo-pretrainer\\data",
        api_key=api_key
        )


def prelabel():
    prelabeler = Prelabeler(
    MODEL_PATH,
    MIN_CONF,
    MAX_CONF,
    IMG_DIR,
    OUTPUT_DIR
    )

    prelabeler.seg_predict(
        conf_threshold=0.7,
        zero_predictions=0,
        overlap_threshold=0.8,
        check_duplicates=1
    )


if __name__ == "__main__":
    main()