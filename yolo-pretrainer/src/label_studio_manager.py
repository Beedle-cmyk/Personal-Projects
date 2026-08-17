from label_studio_converter.brush import mask2rle
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

    def __init__(self, data_dir, ls_path):
        """
        Initializes blah
        """
        self.data_dir = Path(data_dir)
        self.ls_path = Path(ls_path)

    def launch(self):
        env = os.environ.copy()
        os.environ["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
        os.environ["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = self.data_dir
        subprocess.run(os.join(self.ls_path, "activate.bat"), env=env, check=True)


    def ls_convert(mask, width, height, mask_threshold=0.5):
        """
        Converts the given mask data with the prediction height & width via Run Length Encoding (rle)
        for Label Studio compataible format

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
