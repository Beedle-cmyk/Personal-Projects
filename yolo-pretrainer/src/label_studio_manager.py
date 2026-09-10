from utils import brush
from label_studio_sdk import LabelStudio
from pathlib import Path
from urllib.parse import unquote

import numpy as np
import cv2
import subprocess
import json
import os
import time
import yaml
import torch

class LabelStudioManager:
    """Class containing utilities for interfacing with label studio
    An instance of label studio must be running in order for API calls to work

    @Author: Sami Ibrahim
    @Version 9-10-2026

    Methods:
        __init__: Initializes the class with the Label Studio API, Data directory and Label Studio executable path
        launch: Launches a new instance of Label Studio
        terminate (INCOMPLETE) :  Terminates the Label Studio process
        new_project: Creates a new Label Studio project
        import_json: Imports a specified formatted label studio json file containing data labels

        seg_json_to_yolo : converts an exported Label Studio json labels file to its .txt label files for training
        ls_convert: converts a mask into (Run-Length Encoded mask) rle format (intended for use with prelabeler class)
        brush_to_yolo:  Convert a Label Studio brush annotation (Run-Length Encoded mask) rle into a YOLO segmentation polygon
        polygon_to_yolo: Convert Label Studio polygon coordinates into YOLO segmentation format

        _load_labels_mapping : creates a label mapping from a project using its data.yaml; internally used with seg_json_to_yolo

    TODO: connect_local_storage: Establishes a local storage connection for a specific project
    """

    LABEL_STUDIO_URL = "http://localhost:8080"
    
    def __init__(self, 
                 api_key : str | Path, 
                 data_dir : str | Path, 
                 ls_path : str | Path, 
                 launch : bool=True
                 ) -> None:
        """
        Initializes the Label Studio API, data and launches the label studio environment if specified

        Args:
            api_key (str): Label Studio unique API key found in user settings
            data_dir (str): Path to data directory 
            ls_path (str): Path to Label Studio exe directory (non-inclusive of executable in path)
            launch (bool): Whether to launch Label Studio upon initialization
        """

        self.data_dir = data_dir
        self.project_id = None
        self.ls_path = ls_path

        if launch:
            self.launch()
            time.sleep(15)  # Wait for Label Studio to start

        self.client = LabelStudio(base_url=self.LABEL_STUDIO_URL, api_key=api_key)
        me = self.client.users.whoami()
        print("username:", me.username)
        print("email:", me.email)


    def launch(self) -> None:
        """
        Launches the Label Studio environment. Will set the data directory if a path exists
        Note: To stop the process, you will need to manually terminate it using the terminate method

        Args:
            None
        
        Returns:
            None
        """

        env = os.environ.copy()
        if self.data_dir is not None:
            env["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
            env["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = self.data_dir

        self.process = subprocess.Popen([os.path.join(self.ls_path, "label-studio.exe")], env=env, cwd=self.ls_path)
        return self.process


    def terminate(self) -> None:
        """
        Terminates the Label Studio process

        Args:
            None

        Returns:
            None
        """
        if hasattr(self, "process"):
            self.process.terminate()
            self.process.wait()
            print("Label Studio process terminated.")


    def create_project(self, title : str, label_config : str | Path) -> int:
        """
        Creates a new label studio project with the provided title and Labelling Interface

        Args:
            title (str): Project Title
            label_config (str | Path): Path to HTML Labelling Interface configuration
        
        Returns:
            integer Project ID generated
        """
        
        project = self.client.projects.create(title=title, label_config=label_config)
        print("Instance Project ID:", project.id)
        self.project_id = project.id
        return project.id


    def import_json(self, project_id : int | None, json_path : str | Path) -> None:
        """
        Imports the provided json file into the specified Project

        Args:
            project_id (int): provided Project ID
            json_path (str | Path): path to json file

        Returns:
            None 
        """

        if project_id is None:
            if self.project_id is None:
                raise ValueError("Error: No existing Project ID detected. Please enter a valid one")
            project_id = self.project_id

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            print("File Not Found\n")
            print("Nothing Imported")

        print("Importing...\n")
        resp = self.client.projects.import_tasks(id=project_id, request=tasks)
        print(resp)


    # def connect_local_storage(self, project_id : int) -> None:
    #     """
    #     Establishes a local storage connection for a specific project using the data directory provided for class initialization

    #     Args :
    #         project_id (int) : specified project id

    #     Returns:
    #         None
    #     """
    #     # storage = self.client.import_storage.local.create(
    #     #     project=project_id,
    #     # )
    #     # sync_result = self.client.import_storage.s3.sync(import_storage.id)
    #     print("Local Storage Connection Created!\n")
    #     print("To import raw ")
    #     pass


    def seg_json_to_yolo(input_file : str | Path, 
                         yolo_project : str | Path,
                         output_dir : str | Path | None=None
                         ) -> None:
        """
        Function for converting a label studio exported segmentation json file into yolo compatible labels .txt files
        Intended for yolo segmentation as yolo does not support automatic conversions for this

        Args:
            input_file (str | Path): the exported label studio 
            yolo_project (str | Path): path to current yolo working project
            output_dir (str | Path | None): the directory to store labels default is None

        Returns:
            None
        """

        labels_mapping = LabelStudioManager._load_labels_mapping(yolo_project)
        skipped_labels = []

        if output_dir is None:
            output_dir = Path(yolo_project) / r"original_data/labels"

        with open(input_file, "r") as f:
            data = json.load(f)

        for task in data:
            image_path = task["data"]["image"]
            if "?d=" in image_path:  # Label studio local storage uses a ?d=5C format for file names
                image_path = image_path.split("?d=")[-1]

            image_path = unquote(image_path)
            image_path = image_path.replace("\\", "/")
            image_name = os.path.splitext(os.path.basename(image_path))[0]

            # Skip image if any annotation was cancelled
            if any(ann.get("was_cancelled", False) for ann in task.get("annotations", [])):
                print(f"Skipping cancelled image: {image_name}")
                continue

            output_lines = []
            for annotation in task.get("annotations", []):
                for item in annotation["result"]:

                    height = item["original_height"]
                    width = item["original_width"]

                    if item.get("type") == "brushlabels":
                        pts = LabelStudioManager.brush_to_yolo(item["value"]["rle"], height, width)
                        class_name = item["value"]["brushlabels"][0]

                    elif item.get("type") == "polygonlabels":
                        pts = LabelStudioManager.polygon_to_yolo(item["value"]["points"])
                        class_name = item["value"]["polygonlabels"][0]
                    else:
                        skipped_labels.append({
                            "task_id": task.get("id"),
                            "type": item.get("type"),
                            "id": item.get("id")
                        })
                        continue

                    # Require at least 3 points
                    if len(pts) < 6:
                        print(f"Skipping empty polygon: " f"{image_name} ({class_name})")
                        continue

                    class_id = LabelStudioManager.mapping_class(class_name, labels_mapping)
                    output_lines.append(f"{class_id} {' '.join(map(str, pts))}")

            output_file = os.path.join(output_dir, f"{image_name}.txt")
            with open(output_file, "w") as f:
                for line in output_lines:
                    f.write(line + "\n")

            print(f"Converted {image_name}.txt " f"({len(output_lines)} objects)")
        print("Conversion completed.")

        if skipped_labels:
            print("\nSkipped labels:")
            for label in skipped_labels:
                print(label)


    def _load_labels_mapping(yolo_project : str | Path) -> dict:
        """
        Loads the label mapping from the data.yaml file in the current project 
        e.g. {0 : Class1, 0 : Class1, 2: Class2, ..., n : Classn}

        Args:
            yolo_project (str | Path) : path to current working yolo project

        Returns:
            label mapping dictionary
        """

        with open(Path(yolo_project) / "data.yaml", "r") as f:
            data = yaml.safe_load(f)

        labels_mapping = {
            i: name
            for i, name in enumerate(data["names"])
        }
        return labels_mapping


    def mapping_class(class_name : str, labels_mapping : dict) -> int:
        """
        Returns the corresponding number/integer ID mapping to a specified class name
        e.g. {0 : Class1, 0 : Class1, 2: Class2, ..., n : Classn} 
        mapping_class(Class2, labels_mapping) -> returns 2

        Args:
            class_name (str) : name of class or label
            labels_mapping (dict) : keys represent class ID, values represent the class name

        Raises:
            ValueError if the class name is not in the provided dictionary
        """
        try:
            return list(labels_mapping.keys())[
                list(labels_mapping.values()).index(class_name)
            ]
        except ValueError:
            raise ValueError(f"Class name '{class_name}' not found in LABELS_MAPPING")
        
    
    def ls_convert(mask : torch.Tensor, width : int, height : int, mask_threshold : float=0.5):
        """
        Converts the given mask data with the prediction height & width via Run Length Encoding (rle)
        Intened for use with prelabeler class

        Args:
            mask: prediction mask data formatted as a tensor
            width: original width of the image
            height: original height of the image
            mask_threshold: determines how tight the mask is (higher for tighter masks)
        
        Returns:
            rle: Run Length Encoding formatted prediction for Label Studio
        """
        # yolo gives a pytorch tensor of shape (H, W) with values between 0 and 1
        # Converting it to a numpy array for openCV (numpy requires )
        mask_np = mask.cpu().numpy()
        # Upscale since yolo does not predict at orig resolution
        mask_np = cv2.resize(mask_np, (width, height), interpolation=cv2.INTER_NEAREST)
        mask_np = (mask_np >= mask_threshold).astype(np.uint8)  # Making a binary mask true/false --> 1/0

        # Label Studio BrushLabels expects 0/255 mask and uses rle
        # rle e.g. 0 255 255 0 0 0  ---> 1 zero, 2 whites, 3 zeros
        ls_mask = mask_np * 255
        return brush.mask2rle(ls_mask)
    

    def brush_to_yolo(rle : list[int], height : int, width : int) -> list[float]:
        """
        Convert a Label Studio brush annotation (Run-Length Encoded mask) into a YOLO segmentation polygon.
        Directly adapted from utilities brush.py https://github.com/HumanSignal/label-studio-converter 
        Copyright 2020 Heartex Licensed under the Apache License, Version 2.0

        Args:
            rle (list[int]) : Label Studio Run-Length Encoded mask data
            height (int) : Original image height in pixels
            width (int) : Original image width in pixels

        Returns : 
            Flattened list of normalized polygon coordinates in YOLO segmentation format: [x1, y1, x2, y2, ...]
        """

        image = brush.decode_rle(rle)
        image = np.reshape(image, [height, width, 4])

        # Alpha channel contains the mask
        image = image[:, :, 3]

        _, mask = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        polygon = []

        for cnt in contours:

            area = cv2.contourArea(cnt)

            # reject only tiny noise
            if area < 5:
                continue

            # simplify contour
            epsilon = 0.005 * cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, epsilon, True)

            for point in cnt:
                x, y = point[0]
                polygon.extend([round(x / width, 6), round(y / height, 6)])
        return polygon


    def polygon_to_yolo(points) -> list[float]:
        """
        Convert Label Studio polygon coordinates into YOLO segmentation format.
        Label Studio polygon annotations store points as percentages of the image dimensions, where both x and y coordinates are in the range
        [0, 100]. YOLO segmentation format requires normalized coordinates in the range [0, 1].

        Directly adapted from utilities brush.py https://github.com/HumanSignal/label-studio-converter 
        Copyright 2020 Heartex Licensed under the Apache License, Version 2.0

        Args:
            points (list[tuple[float, float]]) : polygon vertices from a label studio annotation
            [(x1, y1), (x2, y2), ...] where x and y are percentages relative to the image size
        
        Returns:
            Flattened list of normalized polygon coordinates in YOLO segmentation format
        """

        polygon = []
        for x, y in points:
            polygon.extend([round(x / 100, 6), round(y / 100, 6)])
        return polygon