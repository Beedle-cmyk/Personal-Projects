from auto_trainer import AutoTrainer


def main():
    autotrain()

def autotrain():

    auto_trainer = AutoTrainer(
        proj_dir=PROJECT_DIRECTORY,
        data_dir=IMG_DIR,
    )

    # auto_trainer.default_prelabel(
    #     model_path=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234\runs\train\weights\best.pt",
    #     min_conf=0.0,
    #     max_conf=1.0,
    #     image_dir=IMG_DIR,
    #     output_dir=Path(PROJECT_DIRECTORY) / r"yolo26_v1.0_seg_234\prelabels"
    # )

    #auto_trainer.update_best_hyperparameters(r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.2_seg_427")
    #auto_trainer.run(current_proj_dir=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.2_seg_427")

    # STEP 0 - Launch Label Studio
    #auto_trainer.studio_launch(ls_path=LABEL_STUDIO_EXE, api_key=API_KEY)


    # # STEP 3 - PRELABEL
    # #auto_trainer.current_proj_dir = r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234"
    # auto_trainer.default_prelabel(
    #     model_path=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234\runs\train\weights\best.pt",
    #     min_conf=0.0,
    #     max_conf=1.0,
    #     image_dir=r"C:\Personal-Projects\yolo-pretrainer\projects\yolo26_v1.0_seg_234\original_data\images",
    # )


if __name__ == "__main__":
    main()