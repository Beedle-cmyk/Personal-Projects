from label_studio_converter.brush import mask2rle
from label_studio_sdk import LabelStudio
from pathlib import Path

import numpy as np
import cv2
import subprocess
import json
import os

class LabelStudioManager:
    """Class containing utilities for interfacing with label studio

    @Author: Sami Ibrahim
    @Version 8-17-2026

    Methods:
        __init__:
        launch:
        new_project:
        import_json:
        ls_convert:
    """

    LABEL_STUDIO_URL = "http://localhost:8080"
    
    def __init__(self, api_key, data_dir):
        """
        Initializes the Label Studio API

        Args:
            api_key (str): Label Studio unique API key found in user settings
            data_dir (str): Path to data directory 
        """
        self.data_dir = data_dir
        self.project_id = None

        self.client = LabelStudio(base_url=self.LABEL_STUDIO_URL, api_key=api_key)
        me = self.client.users.whoami()
        print("username:", me.username)
        print("email:", me.email)



    def launch(self, ls_path) -> None:
        """
        Launches the Label Studio environment
        Will set the data directory if a path exists

        Args:
            ls_path (str): Path to Label Studio exe directory (non-inclusive of executable in path)
        
        Returns:
            None
        """

        env = os.environ.copy()
        if self.data_dir is not None:
            env["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
            env["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = self.data_dir

        subprocess.run([os.path.join(ls_path, "label-studio.exe")], env=env, cwd=self.ls_path, check=True)



    def new_project(self, title, label_config) -> int:
        """
        Creates a new label studio project

        Args:
            title (str): Project Title
            label_config (str): HTML Labelling Interface configuration
        
        Returns:
            integer Project ID generated
        """
        project = self.client.projects.create(title=title, label_config=label_config)
        print("Instance Project ID:", project.id)
        self.project_id = project.id
        return project.id



    def import_json(self, project_id, json_path) -> None:
        """
        Imports the provided json file into the project provided

        Args:
            project_id (int): provided Project ID
            json_path: path to json file

        Returns:
            None 
        """

        with open(json_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        print("Importing...\n")
        resp = self.client.projects.import_tasks(id=project_id, request=tasks)
        print(resp)



    def connect_local_storage(self, project_id):
        # storage = self.client.import_storage.local.create(
        #     project=project_id,
        # )
        # sync_result = self.client.import_storage.s3.sync(import_storage.id)
        pass



    def ls_convert(mask, width, height, mask_threshold=0.5):
        """
        Converts the given mask data with the prediction height & width via Run Length Encoding (rle)

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
        return mask2rle(ls_mask)