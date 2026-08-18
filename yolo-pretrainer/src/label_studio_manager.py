from label_studio_converter.brush import mask2rle
from label_studio_sdk import LabelStudio
from pathlib import Path

import numpy as np
import cv2
import subprocess
import os

class LabelStudioManager:
    """Class containing utilities for interfacing with label studio

    @Author: Sami Ibrahim
    @Version 8-17-2026

    Methods:
    """

    LABEL_STUDIO_URL = "http://localhost:8080"
    
    def __init__(self, data_dir, ls_path, api_key):
        """
        Initializes blah
        """
        self.data_dir = Path(data_dir)
        self.ls_path = Path(ls_path)
        self.client = LabelStudio(base_url=self.LABEL_STUDIO_URL, api_key=api_key)
        me = self.client.users.whoami()
        print("username:", me.username)
        print("email:", me.email)


    def launch(self) -> None:
        """
        Launches the label studio environment with the set data directory
        """
        env = os.environ.copy()
        os.environ["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
        os.environ["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = self.data_dir
        subprocess.run(os.join(self.ls_path, "activate.bat"), env=env, check=True)

    def set_project_id(self, project_id):
        self.project_id = project_id


    def new_project(self, title, label_config) -> None:
        """
        Creates a new label studio project

        Args:
            title (str): Project Title
            label_config (str): HTML Labelling Interface configuration
        """
        project = self.client.projects.create(title=title, label_config=label_config)
        print("Project ID:", project.id)
        return project.id

    def connect_local_storage(self, project_id):
        storage = self.client.import_storage.local.create(
            project=project_id,
        )
        sync_result = self.client.import_storage.s3.sync(import_storage.id)

    def import_json(self, project_id, tasks):
        resp = self.client.projects.import_tasks(id=project_id, request=tasks, return_task_ids=True)
        print(resp)

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
