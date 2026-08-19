from ultralytics import YOLO

class Trainer:
    """ Class for training model

    @author: Sami Ibrahim
    @version: 8/19/2026

    Methods:
        __init__:
    """

    def __init__(self, model):
        """
        Initializes blah

        Args:
            model: pre-trained model to load
        """
        self.model = YOLO(model)
