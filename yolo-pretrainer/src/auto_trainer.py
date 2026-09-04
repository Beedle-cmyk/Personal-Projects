from project_manager import ProjectManager
from trainer import Trainer
from evaluator import Evaluator
from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager
from pathlib import Path

import os
import yaml

class AutoTrainer:
    """ Manager class where all the magic happens folks

    @author: Sami Ibrahim
    @version: 8/21/2026
    
    Methods:
        __init__:
    """

    def __init__(self, proj_dir : str | Path, data_dir : str | Path, current_proj_dir : str | Path | None=None):
        # Primitive Attributes
        self.data_dir = data_dir
        self.current_proj_dir = current_proj_dir
        self.model = None
        self._studio_running = False

        # Object Attributes
        self.project_manager = ProjectManager(proj_dir)
        self.trainer = Trainer()
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
            original_data = Path(self.current_proj_dir) / "original_data"

            LabelStudioManager.seg_json_to_yolo(label_json, original_data / "labels", 
                                                LabelStudioManager.load_labels_mapping(self.current_proj_dir))

            label_count = sum(1 for item in (original_data / "labels").iterdir() if item.is_file())
            file_count = self.project_manager.count_data(original_data)

            if label_count < file_count:
                self.cleanup_images(original_data / "labels", original_data / "images")
                original_data = Path(self.current_proj_dir) / "original_data"  #updated names for resize
                yaml_dir = Path(self.current_proj_dir) / "data.yaml"
            elif label_count > file_count:
                raise ValueError(f"WARNING: More Labels than Image files. Please Check {original_data}")

            self.trainer.stratified_split(data_dir=original_data, data_yaml=yaml_dir, output_dir=self.current_proj_dir)



    def cleanup_images(self, labels_dir : (str | Path), images_dir : (str | Path)) -> None:
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
        total = 0

        for image_file in os.listdir(images_dir):
            if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_name = normalize(os.path.splitext(image_file)[0])
                total +=1

                if image_name not in label_names:
                    image_path = os.path.join(images_dir, image_file)
                    os.remove(image_path)
                    print("Deleted:", image_file)
                    deleted += 1

        remaining = total - deleted

        dataset_dir = Path(images_dir).parent.parent
        parts = str(dataset_dir.name).split("_")
        parts[-1] = str(remaining)
        rejoined = "_".join(parts)

        self.current_proj_dir = dataset_dir.rename(dataset_dir.parent / rejoined)

        self.project_manager.update_yaml_paths(self.current_proj_dir)
        print(f"Done. Deleted {deleted} images.")

                

    def run(self, current_proj_dir: str | Path | None=None, args_yaml : str | Path | None=None, tune : bool=False):
        """
        Default training method that creates a new project and trains the model with the provided args.yaml file
        Tuner is implemented if set to true will begin/resume the tuning process

        Args:
            current_proj_dir (str | Path): current project directory
            args_yaml (str | Path): optional path to the args.yaml file containing training parameters
            tune (bool) : if true will begin or resume hyperparameter tuning
        
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
            args_yaml = Path(self.current_proj_dir) / "cfg/tune_args.yaml" if tune else Path(self.current_proj_dir) / "cfg/args.yaml"

        if tune:
            self.model = self.trainer.tune(cfg=args_yaml, current_project_dir=current_proj_dir)

        else:
            self.model = self.trainer.train(cfg=args_yaml, current_project_dir=current_proj_dir)



    def default_prelabel(self, model_path, min_conf, max_conf, image_dir, output_dir=Path.cwd()):
        """
        Args:
            model_path (str | Path): Path to the model file you would like to prelabel with (.pt file)
            min_conf (float): minimum confidence threshold
            max_conf (float): maximum confidence threshold
            image_dir (str | Path): path to data to prelabel (default is current directory)
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

        self.label_studio_manager = LabelStudioManager(api_key=api_key, data_dir=self.data_dir, ls_path=ls_path, launch=False)
        self._studio_running = True
        # self.proj_id = self.label_studio_manager.create_project(title=Path(self.current_proj_dir).path.name, label_config=label_config)
        # self.label_studio_manager.import_json(self.proj_id, Path(self.current_proj_dir) / "prelabels/seg_predictions.json")


    def update_best_hyperparameters(self, current_proj_dir: str | Path, yaml_path: str | Path | None = None, 
                                    args_yaml: str | Path | None=None) -> None:
        """
        Update args.yaml with tuned hyperparameters.
        """
        exclude = {"epochs", "imgsz", "batch"}

        if args_yaml is None:
            args_yaml = Path(current_proj_dir) / "cfg/args.yaml"

        if yaml_path is None:
            yaml_files = list((Path(current_proj_dir) / "runs").rglob("best_hyperparameters.yaml"))
            if not yaml_files:
                raise FileNotFoundError("No best_hyperparameters.yaml found.")
            latest_yaml = max(yaml_files, key=lambda p: p.stat().st_mtime)
            print(f"No best_hyperparameters.yaml provided. Using most recent: {latest_yaml}")
        else:
            latest_yaml = Path(yaml_path)

        with open(latest_yaml, "r") as f:
            best_hyp = yaml.safe_load(f)

        with open(args_yaml, "r") as f:
            args_data = yaml.safe_load(f)

        for key, value in best_hyp.items():
            if key in exclude:
                continue
            if key in args_data:
                args_data[key] = value

        with open(args_yaml, "w") as f:
            yaml.safe_dump(args_data, f, sort_keys=False)
        print(f"Updated {args_yaml} with tuned hyperparameters.")