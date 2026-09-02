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
    
    Methods:
        __init__:
    """

    def __init__(
            self,
            proj_dir : str | Path,
            data_dir : str | Path,
        ):
        # Primitive Attributes
        self.data_dir = data_dir
        self.current_proj_dir = None
        self.model = None

        # Object Attributes
        self.project_manager = ProjectManager(proj_dir)
        self.trainer = Trainer()
        #self.evaluator = Evaluator(self.project_manager)
        #self.prelabeler = Prelabeler()
        
    

    def setup_project(self, label_json=None, label_config=None):
        """
        Sets up a new project by creating the necessary directory structure and converting Label Studio JSON labels to YOLO format if provided

        Args:
            label_json (str | Path): Path to the Label Studio labels exported json file
            label_config (str | Path): Optional path to the Label Studio label class configuration file (default is None)

        Returns:
            None
        """

        self.project_manager.create_project(data_dir=self.data_dir, label_config=label_config)
        self.current_proj_dir = self.project_manager.current_proj

        if label_json:
            original_data = Path(self.project_manager.current_proj) / "original_data"
            yaml_dir = Path(self.project_manager.current_proj) / "data.yaml"

            LabelStudioManager.seg_json_to_yolo(label_json, original_data / "labels", self.load_labels_mapping())
            self.trainer.stratified_split(data_dir=original_data, data_yaml=yaml_dir, output_dir=self.project_manager.current_proj)

        

    def default_train(self, current_proj_dir=None, args_yaml=None):
        """
        Default training method that creates a new project and trains the model with the provided args.yaml file

        Args:
            current_proj_dir (str | Path): current project directory
            args_yaml (str | Path): optional path to the args.yaml file containing training parameters
        
        Returns:
            None
        """
        if current_proj_dir is None:
            if self.current_proj_dir is None:
                raise ValueError("No Valid Project Directory provided")
            current_proj_dir = self.current_proj_dir
        else:
            self.current_proj_dir = current_proj_dir
        
        if args_yaml is None:
            args_yaml = Path(self.current_proj_dir) / "cfg/args.yaml"

        self.model = self.trainer.train(cfg=args_yaml, current_project_dir=current_proj_dir) 



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

        

    def load_labels_mapping(self):
        """
        Loads the label mapping from the data.yaml file in the current project directory

        Args:
            None

        Returns:
            None
        """

        with open(Path(self.project_manager.current_proj) / "data.yaml", "r") as f:
            data = yaml.safe_load(f)

        labels_mapping = {
            i: name
            for i, name in enumerate(data["names"])
        }
        return labels_mapping