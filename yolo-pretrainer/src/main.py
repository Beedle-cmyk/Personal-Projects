from prelabeler import Prelabeler

MODEL_PATH = r"C:\Personal-Projects\yolo-pretrainer\models\YOLO\best.pt"
IMG_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\images"
OUTPUT_DIR = r"C:\Personal-Projects\yolo-pretrainer\data\outputs"

MIN_CONF = 0.0
MAX_CONF = 1.0


def main():
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