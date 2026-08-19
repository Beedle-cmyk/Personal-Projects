from ultralytics import YOLO
from pathlib import Path
from label_studio_manager import LabelStudioManager
from tqdm import tqdm

import json
import os

class Prelabeler:
    """Base class for prelabelling image datasets using YOLO/RFDETR models

    Specifically designed to generate predictions in a format compatible with Label Studio.
    Tested with sequential video frame extraction and analysis
    TODO: 
        Inspect Studio integration
        Prediction statistics: Overlapped, Low Conf, Zero, Duplicates detected etc.
        Save points every n mins

    @Author: Sami Ibrahim
    @Version 8-14-2026

    Methods:
        __init__:
        _initialize_model:
        set_confidence:
        _mask_overlap:

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



    def box_iou(self, box1, box2) -> float:
        """
        Computes the Intersection over Union (IoU) between two prediction boxes

        Args:
            box1 : First prediction box
            box2 : Second prediction box
        
        Returns:
            The computed IoU between both boxes
        """

        inter_x1 = max(box1[0], box2[0])
        inter_y1 = max(box1[1], box2[1])
        inter_x2 = min(box1[2], box2[2])
        inter_y2 = min(box1[3], box2[3])

        intersection = (max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1))

        area1 = (max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1]))
        area2 = (max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1]))

        union = area1 + area2 - intersection
        return intersection / union if union > 0 else 0.0



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
        maski1 = mask1.bool()
        maski2 = mask2.bool()

        # Counting the intersections
        intersection = (maski1 & maski2).sum().float()

        area1 = maski1.sum().float()
        area2 = maski2.sum().float()
        smaller_area = min(area1, area2)

        if smaller_area == 0:
            return 0.0   # dont divide by 0
        
        return (intersection / smaller_area).item()  # item() to convert from tensor decimal to float



    def check_overlap(self, masks, boxes, overlap_threshold, iou_threshold=0.05) -> bool:
        """
        Checks if there is overlap between the provided prediction image

        Args:
            masks:
            boxes:
            overlap_threshold:
            iou_threshold:
        
        Returns:

        """

        for i in range(len(masks)):
            cls_i = int(boxes[i].cls[0])

            for j in range(i + 1, len(masks)):
                cls_j = int(boxes[j].cls[0])

                if cls_i != cls_j:
                    continue 
                
                if self.box_iou(boxes[i].xyxy[0], boxes[j].xyxy[0]) < iou_threshold:
                    continue

                overlap = self._mask_overlap(masks[i], masks[j])
                if overlap >= overlap_threshold:
                    return True
        return False



    def same_prediction(self, prev_boxes, curr_boxes, iou_threshold=0.90) -> bool:
        """
        Checks if two frames have essentially the same detections

        Args:
            prev_boxes: The bounding boxes of the first image prediction
            curr_boxes: The bounding boxes of the second image prediction
            iou_threshold: IoU threshold that must be met to classify as same detection

        Returns:
            True when both boxes predictions possess the same class, label number and IoU
            is greater than the provided threshold
        """

        if len(prev_boxes) != len(curr_boxes):
            return False

        if len(prev_boxes) == 0:
            return True

        prev_classes = [int(box.cls[0]) for box in prev_boxes]
        curr_classes = [int(box.cls[0]) for box in curr_boxes]

        if prev_classes != curr_classes:
            return False

        for prev_box, curr_box in zip(prev_boxes, curr_boxes):
            iou = self.box_iou(prev_box.xyxy[0].tolist(), curr_box.xyxy[0].tolist())
            if iou < iou_threshold:
                return False
        return True



    def seg_predict(self, conf_threshold=0.0, zero_predictions=False, overlap_threshold=0.0, check_duplicates=False) -> None:
            """
            Predicts segmentation labels for images in the specified directory using the initialized model. 
            Saves the predictions in a JSON file compatible with Label Studio.
            Assumes image video/frames are sequential for duplicate filtering

            When parameters set filteres a segmentation/mask dataset for manual review and adds 
            images with the following behavior to a review dataset

            Args:
                conf_threshold (float): flags images with predictions below this confidence score
                zero_predictions (bool): when true reviews images with no predictions with SAM3
                overlap_threshold (float): flags images that contain overlapping masks to a percentage degree e.g. 80% overlap
                check_duplicates (bool): when true skip images that appear to be duplicates

            Returns:
                None
            """

            tasks = []
            prev_boxes = None

            image_files = [ p for p in self.image_dir.rglob("*") if p.suffix.lower() in self.SUPPORTED_IMG_EXTENSIONS]
            review_mode = (conf_threshold > 0.0 or overlap_threshold > 0.0 or zero_predictions)

            for image_path in tqdm(image_files, desc="Processing Images"):
                
                prediction = self.model(str(image_path))[0]
                height, width = prediction.orig_shape  # e.g. if the image was resized to 640x640, this will be 640, 640

                # CHECK 1 - No detections
                if prediction.masks is None:
                    # if not review_mode:
                    #     continue
                    # if zero_predictions:
                    #     #TODO SAM3
                    continue

                masks = prediction.masks.data
                boxes = prediction.boxes

                # CHECK 2 - Similar consecutive video frames
                if check_duplicates and prev_boxes is not None:
                    if self.same_prediction(prev_boxes, boxes, iou_threshold=0.90):
                        continue  # Skip that image
                prev_boxes = boxes

                # CHECK 3 - Overlapping labels
                overlap_flag = False
                if overlap_threshold > 0.0:
                    overlap_flag = self.check_overlap(masks, boxes, overlap_threshold)

                # CHECK 4 - Low Confidence
                lowconf_flag = False
                if conf_threshold > 0.0:
                    lowconf_flag = any(float(box.conf[0]) < conf_threshold for box in boxes)

                review_image = overlap_flag or lowconf_flag
                if review_mode and not review_image:
                    continue

                results = []

                # zip -> (mask1, box1) then enumerate -> (0, (mask1, box1)) (1, (mask2, box2)) ...)
                # mask contains the segmentation mask for the object (pixel map)
                # box contains the class ID, confidence score, and bounding box coordinates
                for i, (mask, box) in enumerate(zip(masks, boxes)):
                    conf = float(box.conf[0])
                    if not(self.min_conf <= conf <= self.max_conf):
                        continue

                    # Mapping the model's class index to the corresponding label name
                    cls = int(box.cls[0])
                    yolo_label = self.model.names[cls]

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

                if not results:
                    continue
    
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