from project_manager import ProjectManager
from trainer import Trainer
from evaluator import Evaluator
from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager
from pathlib import Path

import yaml

class AutoTrainer:
    """ Manager class where all the magic happens folks

    @author: Sami Ibrahim
    @version: 8/21/2026
    
    """

    DEFAULT_PROJECT_DIR = r"..\projects"

    def __init__(
            self,
            proj_dir : str | Path,
            data_dir : str | Path,
        ):
        # Primitive Attributes
        self.data_dir = data_dir
        self.model = None

        # Object Attributes
        self.project_manager = ProjectManager(proj_dir)
        #self.evaluator = Evaluator(self.project_manager)
        #self.prelabeler = Prelabeler()
        #self.trainer = Trainer()
        

    def default_train(self, args_yaml="args.yaml"):
        """
        Default training method that creates a new project and trains the model with the provided args.yaml file

        Args:
            args_yaml (str): Path to the args.yaml file containing training parameters
        
        Returns:
            None
        """

        self.project_manager.create_project(data_dir=self.data_dir)
        self.model = self.trainer.train(cfg=args_yaml) 



    def studio_launch(self, api_key, ls_path) -> None:
        """
        Launches the Label Studio environment for reviewing and editing labels

        Args:
            api_key (str): Label Studio unique API key found in user settings
            ls_path (str | Path): Path to Label Studio exe directory (non-inclusive of executable in path)
        
        Returns:
            None
        """

        self.label_studio_manager = LabelStudioManager(api_key=api_key, data_dir=self.data_dir, ls_path=ls_path)
        

    def start(self, labels_json, model: str | Path,):
        self.project_manager.create_project(name="auto-train_" + self.trainer.model, data_dir=self.data_dir)

        labels_mapping = self.load_labels_mapping()

        labels_folder = self.project_manager.current_proj + "/original_data/labels"
        self.label_studio_manager.seg_json_to_yolo(labels_json, labels_folder, labels_mapping)

        #STEP 1 - initial training try out 3 fixed param configurations to get imgsz, batch size and epoch number
        self.trainer.train(cfg="")
        self.trainer.tune()

        paramsets = self.evaluator.params()
        self.trainer.train(paramsets)
        self.evaluator.generate_report()
        self.prelabeler.seg_predict()
        self.label_studio_manager.launch()
        self.label_studio_manager.import_json()
        # Review on labelstudio
    

    def load_labels_mapping(self):
    
        with open(self.project_manager.current_proj + "/data.yaml", "r") as f:
            data = yaml.safe_load(f)

        labels_mapping = {
            i: name
            for i, name in enumerate(data["names"])
        }
        return labels_mapping