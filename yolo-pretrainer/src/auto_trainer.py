from project_manager import ProjectManager
from trainer import Trainer
from evaluator import Evaluator
from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager
from pathlib import Path

import os

class AutoTrainer:
    """ Manager class where all the magic happens folks

    @author: Sami Ibrahim
    @version: 8/21/2026
    
    Methods:
        __init__:
    """

    def __init__(self, proj_dir : str | Path, data_dir : str | Path,):
        # Primitive Attributes
        self.data_dir = data_dir
        self.current_proj_dir = None
        self.model = None
        self._studio_running = False

        # Object Attributes
        self.project_manager = ProjectManager(proj_dir)
        self.trainer = Trainer()
        self._studio_thread = None
        self._label_studio_manager = None
        #self.evaluator = Evaluator(self.project_manager)
        

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

            LabelStudioManager.seg_json_to_yolo(label_json, original_data / "labels", 
                                                LabelStudioManager.load_labels_mapping(self.current_proj_dir))

            label_count = sum(1 for item in (original_data / "labels").iterdir() if item.is_file())
            file_count = self.project_manager.count_data(original_data)

            if label_count < file_count:
                AutoTrainer.cleanup_images(original_data / "labels", original_data / "images")
            elif label_count > file_count:
                raise ValueError(f"WARNING: More Labels than Image files. Please Check {original_data}")

            self.trainer.stratified_split(data_dir=original_data, data_yaml=yaml_dir, output_dir=self.project_manager.current_proj)



    def cleanup_images(labels_dir : (str | Path), images_dir : (str | Path)) -> None:
        """
        Helper Method for providing cleaning up data such that the label/class count matches the data count

        Args:
            labels_dir (str | Path): label/class directory
            images_dir (str | Path): data directory

        Returns:
            None
        """

        # Function to normalize names (remove "-something")
        def normalize(name): return name.split("-")[0].lower()

        # Get normalized label names
        label_names = {
            normalize(os.path.splitext(f)[0])
            for f in os.listdir(labels_dir)
            if f.endswith(".txt")
        }

        deleted = 0

        for image_file in os.listdir(images_dir):
            if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_name = normalize(os.path.splitext(image_file)[0])

                if image_name not in label_names:
                    image_path = os.path.join(images_dir, image_file)
                    os.remove(image_path)
                    print("Deleted:", image_file)
                    deleted += 1

        print(f"Done. Deleted {deleted} images.")

                

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



    def default_prelabel(self, model_path, min_conf, max_conf, image_dir, output_dir=Path.cwd()):
        """
        Args:
            model_path (str | Path): Path to the model file
            min_conf (float): minimum confidence threshold
            max_conf (float): maximum confidence threshold
            image_dir (str | Path): path to data to prelabel
        """
        prelabeler = Prelabeler(
            model_path=model_path,
            min_conf=min_conf,
            max_conf=max_conf,
            image_dir=image_dir,
            output_dir=output_dir
        )

        if self.current_proj_dir is not None:
            prelabeler.output_dir = Path(self.current_proj_dir) / "prelabels"

        prelabeler.seg_predict()



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
        # self.proj_id = self.label_studio_manager.create_project(title=Path(self.current_proj_dir).path.name, label_config=label_config)
        # self.label_studio_manager.import_json(self.proj_id, Path(self.current_proj_dir) / "prelabels/seg_predictions.json")