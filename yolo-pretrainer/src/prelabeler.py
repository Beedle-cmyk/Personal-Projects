from ultralytics import YOLO
from pathlib import Path
from label_studio_manager import LabelStudioManager
from tqdm import tqdm

import json
import cv2
import hashlib
import os

class Prelabeler:
    """Base class for prelabelling image datasets using YOLO/RFDETR models

    Specifically designed to generate predictions in a format compatible with Label Studio.
    TODO: Inspect Studio integration

    @Author: Sami Ibrahim
    @Version 8-14-2026

    Methods:
        __init__:
        _initialize_model:
        set_confidence:
        _mask_overlap:
        _pixel_hash:

    """

    SUPPORTED_MODELS = {
        "YOLO" : "ultralytics YOLO",
        "RFDETR" : "Roboflow RFDETR"
    }

    SUPPORTED_IMG_EXTENSIONS = {
        ".jpg", 
        ".jpeg", 
        ".png"
    }


    def __init__(self, model_path, min_conf, max_conf, image_dir, output_dir="."):
        """
        Initializes the Prelabeler with the specified model path, confidence threshold 
        and image directory.

        Args:
            model_path (str | Path): Path to the model file
            min_conf (float): minimum confidence threshold
            max_conf (float): maximum confidence threshold
            image_dir (str | Path): path to image data directory
        """
        
        self.model = self._initialize_model(model_path)
        self.set_confidence(min_conf, max_conf)
        self.image_dir = Path(image_dir)
        self.output_dir = Path(output_dir)
        #TODO output Directory check if exists


    def _initialize_model(self, model_path) -> YOLO:
        """
        Initialize a model from the provided model path.

        Supports YOLO and RFDETR models.

        Args:
            model_path (str | Path): Path to the model file

        Raises:
            ValueError: If the model type is unsupported or the model fails to initialize

        Returns:
            Model: Initialized model instance
        """

        if model_path is None:
            raise ValueError("Model path is not provided. Please provide a valid model path.")
        
        if model_path.endswith(".pt"):
            print(f"Model '{model_path}' initialized successfully.")
            return YOLO(model_path)
        
        # elif model_path.endswith(".pth"):
        #     self.model = RFDETR(model_path)
        else:
            raise ValueError(f"Model is not supported. Supported models are: {list(self.SUPPORTED_MODELS.keys())}")

        
    def set_confidence(self, min_conf, max_conf) -> None:
        """
        Sets the confidence threshold (max and min confidence values)

        Args:
            min_conf (float): minimum confidence score
            max_conf (float): maximum confidence score

        Raises:
            ValueError: If the confidence threshold is not between 0 and 1

        Returns:
            None
        """
        if not (0 <= min_conf <= 1 and 0 <= max_conf <= 1):
            raise ValueError("Confidence threshold must be between 0 and 1.")
        
        self.min_conf = min_conf
        self.max_conf = max_conf
        print(f"Minimum confidence threshold set to {self.min_conf}")
        print(f"Maximum confidence threshold set to {self.max_conf}")


    def _mask_overlap(self, mask1, mask2) -> float:
        """
        Calculates an overlap percentage float between the two provided masks

        Similar to IoU (Intersection Over Union) but instead divides by the smaller
        area instead of the two masks for overlap

        Args:
            mask1, mask2:

        Returns:
            float representing an overlap percentage between mask1 and mask2
        """
        # Convert to bool for logical operations
        mask1 = mask1.bool()
        mask2 = mask2.bool()

        # Counting the intersections
        intersection = (mask1 & mask2).sum().float()

        area1 = mask1.sum().float()
        area2 = mask2.sum().float()
        smaller_area = min(area1, area2)

        if smaller_area == 0:
            # dont divide by 0
            return 0.0
        
        return (intersection / smaller_area).item()  # item() to convert from tensor decimal to float


    def _pixel_hash(self, image_path) -> str:
        """
        Computes and returns the SHA-256 hash of the provided image
        For use in filtering exact image duplicates

        Args:
            image_path: path to the image to compute
        
        Returns:
            SHA-256 hash string of image provided
        """
        img = cv2.imread(str(image_path))
        return hashlib.sha256(img.tobytes()).hexdigest()

    
    def seg_predict(self, conf_threshold=0.0, zero_predictions=0, overlap_threshold=0.0, check_duplicates=0) -> None:
        """
        Predicts segmentation labels for images in the specified directory using the initialized model. 
        Saves the predictions in a JSON file compatible with Label Studio.

        When parameters set filteres a segmentation/mask dataset for manual review and adds 
        images with the following behavior to a review dataset

        Args:
            conf_threshold (float): flags images with predictions below this confidence score
            zero_predictions (bool): when true reviews images with no predictions with SAM3
            overlap_threshold (float): flags images that contain overlapping masks to a percentage degree e.g. 80% overlap
            check_duplicates (bool): when true ignores potential duplicate images

        Returns:
            None
        """

        tasks = []
        seen_hashes = set()

        if conf_threshold < self.min_conf:
            conf_threshold = self.min_conf
    
        # Loop through all images in the directory recursively and make predictions
        image_files = [ p for p in self.image_dir.rglob("*") if p.suffix.lower() in self.SUPPORTED_IMG_EXTENSIONS]

        for image_path in tqdm(image_files, desc="Processing Images"):
            results = []
            overlap_flag = False
            lowconf_flag = 1 if conf_threshold == 0.0 else 0

            # CHECK 1 - Duplicate Images
            if check_duplicates:
                pixel_hash = self._pixel_hash(image_path)

                if pixel_hash in seen_hashes:
                    #print(f"Skipping duplicate frame: {image_path}")
                    continue

                seen_hashes.add(pixel_hash)

            if image_path.suffix.lower() not in self.SUPPORTED_IMG_EXTENSIONS:
                continue 
            #print(f"Processing {image_path}")

            prediction = self.model(str(image_path))[0]
            height, width = prediction.orig_shape  # e.g. if the image was resized to 640x640, this will be 640, 640

            # CHECK 2 - No detections
            if prediction.masks is None:
                #print(f"No masks found for {image_path}")
                if zero_predictions:
                    #TODO: SAM3 Check
                    continue
                continue

            # CHECK 3 - Overlapping labels
            if overlap_threshold > 0.0:
                masks = prediction.masks.data
                boxes = prediction.boxes

                for i in range(len(masks)):
                    cls_i = int(boxes[i].cls[0])

                    for j in range(i + 1, len(masks)):
                        cls_j = int(boxes[j].cls[0])

                        if cls_i != cls_j:
                            continue  # Only check overlap if same class

                        overlap = self._mask_overlap(masks[i], masks[j])
                        if overlap >= overlap_threshold:
                            overlap_flag = True
                            #print(f"Overlap detected: " f"{image_path.name} " f"class={self.model.names[cls_i]} " f"overlap={overlap:.2f}")
                            break
                        
                    if overlap_flag:
                        break
                
            # zip -> (mask1, box1) then enumerate -> (0, (mask1, box1)) (1, (mask2, box2)) ...)
            # mask contains the segmentation mask for the object (pixel map)
            # box contains the class ID, confidence score, and bounding box coordinates
            for i, (mask, box) in enumerate(zip(prediction.masks.data, prediction.boxes)):
                conf = float(box.conf[0])
                if not(self.min_conf <= conf <= self.max_conf):
                    continue

                # Mapping the model's class index to the corresponding label name
                cls = int(box.cls[0])
                yolo_label = self.model.names[cls]

                # CHECK 4 - Low Confidence
                if conf < conf_threshold:
                    lowconf_flag = 1
                    #print(f"Low Conf detected: " f"{image_path.name}" f"class={yolo_label}")

                rle = LabelStudioManager.ls_convert(mask, width, height)

                results.append({
                    "id": f"{image_path.stem}_{i}",
                    "from_name": "tag",
                    "to_name": "image",
                    "type": "brushlabels",
                    "score": conf,
                    "original_width": width,
                    "original_height": height,
                    "image_rotation": 0,
                    "value": {
                        "format": "rle",
                        "rle": rle,
                        "brushlabels": [yolo_label]
                    }
                })

            if lowconf_flag or overlap_flag:
                tasks.append({
                    "data": {"image": f"/data/local-files/?d=images%5C{image_path.name}"},
                    "predictions": [{
                        "model_version": "1.0.0",
                        "score": max([r["score"] for r in results], default=0),
                        "result": results
                    }]
                })

        with open(os.path.join(self.output_dir, "seg_predictions.json"), "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        print(f"Saved {len(tasks)} tasks to {self.output_dir} seg_predictions.json")


    def box_predict(self):
        """
        Predicts box labels for images in the specified directory using the initialized model. 
        Saves the predictions in a JSON file compatible with Label Studio.

        Args:
            None

        Returns:
            None
        """

        tasks = []
        for image_path in self.image_dir.rglob("*"):

            if image_path.suffix.lower() not in self.SUPPORTED_IMG_EXTENSIONS:
                continue
            print(f"Processing {image_path}")

            prediction = self.model(str(image_path))[0]
            height, width = prediction.orig_shape

            results = []

            for i, box in enumerate(prediction.boxes):

                conf = float(box.conf[0])
                if not(self.min_conf <= conf <= self.max_conf):
                    continue

                cls = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                yolo_label = self.model.names[cls]

                results.append({
                    "id": f"{image_path.stem}_{i}",
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "score": conf,
                    "value": {
                        "x": (x1 / width) * 100,
                        "y": (y1 / height) * 100,
                        "width": ((x2 - x1) / width) * 100,
                        "height": ((y2 - y1) / height) * 100,
                        "rotation": 0,
                        "rectanglelabels": [yolo_label]
                    }
                })

            tasks.append({
                "data": {
                    "image": f"/data/local-files/?d=images%5C{image_path.name}"
                },
                "predictions": [{
                    "model_version": "1.0.0",
                    "score": max([r["score"] for r in results], default=0),
                    "result": results
                }]
            })

        with open(os.path.join(self.output_dir, "box_predictions.json"), "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        print(f"\nSaved {len(tasks)} tasks to {self.output_dir} box_predictions.json")