from pathlib import Path
from config import (CFG_DIRECTORY)

import xml.etree.ElementTree as ET

import os
import shutil
import yaml

class ProjectManager:
    """Class for creating and managing YOLO projects under my custom defined
    project structure 

    @author: Sami Ibrahim
    @version: 8/20/2026

    Methods:
        __init__: Initializes class project attributes
        create_project: creates a new project with pre-defined structure

        update_findings: Updates findings.txt (INCOMPLETE) TODO Evaluator class integration
        count_data: counts the amount of data stored for a specific project
        get_labels_from_config : Extracts labels from the LabelStudio Formatted xml configuration file for classes
        update_yaml_paths : Updates the yaml paths to map to the current directory

        _update_cfgs : Updates the yaml configuration files with the correct pathing
    """

##############################################
    FINDINGS_TEMPLATE = """Best Model: 
    
Version:

--------------------------------
|        Version Updates       |
--------------------------------
-


--------------------------------
|          Findings            |
--------------------------------
-"""
################################################

################################################
    DATA_YAML_TEMPLATE = """path:
train: train\\images
val: val\\images

nc: 3

names: ["Class1", "Class2", "Class3"]"""
################################################

    SUPPORTED_IMG_EXTENSIONS = {
        ".jpg", 
        ".jpeg", 
        ".png"
    }

    SUPPORTED_PROJECT_TYPES = {
        "box",
        "seg"
    }
    
    def __init__(self, project_dir : str | Path) -> None:
        """
        Initializes a path to the project directory, along with other project-related attributes

        Args:
            project_dir (str | Path): path to where projects are stored
            data_num (int): total number of data files for a specific project (initialized to 0)
            current_proj (str | Path): path to current working project (initialized to None)

        Returns:
            None
        """

        self.project_dir = Path(project_dir)
        self.current_proj = None
        self.data_num = 0


    def create_project(self, 
                       name : str | None = None, 
                       data_dir : str | Path | None = None, 
                       version : float | None = None, 
                       project_type : str = "seg", 
                       yolo_version : str = "yolo26", 
                       label_config : str | None =None
                       ) -> Path:
        """
        Creates a new project within the project directory with my own custom pre-defined structure 
        Will autofill parameters if set to none or not filled so calling create_project() alone will work fine
        Only recommendation would be filling out the data_dir
        
        example:
        Project Directory --- yolo26_v1.2_box_400 ----- original_data ------ images
                                                     |                ------ labels               
                                                     |
                                                     |- prelabels 
                                                     |
                                                     |- runs
                                                     |
                                                     |- cfg ------ args.yaml
                                                     |      ------ tune_args.yaml
                                                     |                    
                                                     |- data.yaml
                                                     |
                                                     |- findings.txt

        original_data/images : the image data from the provided data directory is stored here 
        original_data/labels : label data is stored here (formated .txt)
        prelabels : prelabels for labelstudio using a trained model are stored here (formated .json)
        runs : training runs are stored in this directory 
        cfg : base yolo argument config files stored here (format .yaml)
        data.yaml : yaml that yolo uses to begin training
        findings.txt : utlines the updates with that version, current best model (of all previous versions) and general findings

        The naming scheme is as follows:

        model_version_detection-type_dataset-size
        model   		:  The specific model trained (e.g. yolo11, yolo7, etc)
        version 		:  A personal revision identifier used to track the iteration or update 
                           level of a work product (e.g., v1.0, v1.1, v1.2). It indicates progress 
                           and changes made over time and does not refer to the underlying model or system version.
        detection-type  :  Bounding Boxes or Semantic Segmentation ("seg" or "box") default is "seg"
        dataset-size    :  Self-explanatory - howmany images are in the dataset
    
        Args:
            name (str): optionally define custom project name if an auto generated name isn't desired
            data_dir (str | Path): directory/location of image data in file system
            version (float): optionally set project version
            project_type (str): define project type, defaults are "seg" or "box"
            yolo_version (str): define yolo version, defaults is "yolo26"
            label_config (str | Path): optionally provide a label class configuration xml file for Label Studio
        
        Raises:
            ValueError if project_type is not supported
            FileExistsError if the project already exists
        
        Returns:
            Path to project created                                 
        """
        print("Starting Project Creation...")

        latest_findings = self.FINDINGS_TEMPLATE
        latest_data_yaml = self.DATA_YAML_TEMPLATE

        if project_type not in self.SUPPORTED_PROJECT_TYPES:
            raise ValueError(f"project_type must be one of " f"{self.SUPPORTED_PROJECT_TYPES}")

        if data_dir is not None:
            data_dir = Path(data_dir)
            self.count_data(data_dir)  # Updates the attribute data_num
        else:
            self.data_num = 0

        if name is None:

            if version is None:  # Auto assign version number if none specified
                version = 0.9
                for project in self.project_dir.iterdir():
                    # Checking to see if the project type and version number already exist
                    if project.is_dir() and project.name.find(project_type) != -1:
                        try:
                            parts = project.name.split("_")
                            curr_version = float(parts[1][1:])  #"v1.2" -> 1.2

                            if version < curr_version:
                                version = curr_version

                                try:
                                    with open(os.path.join(project, "findings.txt"), "r") as f:
                                        latest_findings = f.read()
                                except FileNotFoundError:
                                    print(f"findings.txt not found in {project.name} Skipping...")

                                try:
                                    with open(os.path.join(project, "data.yaml"), "r") as f:
                                        latest_data_yaml = f.read()
                                except FileNotFoundError:
                                    print(f"data.yaml not found in {project.name} Skipping...")

                        except (IndexError, ValueError):
                            continue
                        
                version = round(version + 0.1, 1)

            full_name = yolo_version + "_v" + str(version) + "_" + project_type + "_" + str(self.data_num)
            working_dir = self.project_dir / full_name

        else:
            working_dir = self.project_dir / name

        if working_dir.exists():
            raise FileExistsError(f"Error {working_dir} already exists")
        working_dir.mkdir()  # Create the project directory

        findings_path = working_dir / "findings.txt"
        self.update_findings(findings_path, latest_findings)  # Create the findings.txt file with the latest findings

        # data.yaml path overwrite
        yaml_lines = latest_data_yaml.splitlines()
        for i, line in enumerate(yaml_lines):
            if line.strip().startswith("path:"):
                yaml_lines[i] = f"path: {working_dir}\\data"
                break
        latest_data_yaml = "\n".join(yaml_lines)

        cfg_dir = working_dir / "cfg"
        cfg_dir.mkdir()  # Create cfg directory for args.yaml
        ProjectManager._update_cfgs(cfg_dir=cfg_dir, working_dir=working_dir, yaml_path=CFG_DIRECTORY / r"args.yaml")
        ProjectManager._update_cfgs(cfg_dir=cfg_dir, working_dir=working_dir, yaml_path=CFG_DIRECTORY / r"tune_args.yaml")

        # Checking if a label config is provided, if so then update the data.yaml with the labels and number of classes
        if label_config is not None:
            labels = ProjectManager.get_labels_from_config(label_config)
            yaml_lines = latest_data_yaml.splitlines()

            for i, line in enumerate(yaml_lines):

                if line.strip().startswith("names:"):
                    yaml_lines[i] = f"names: {labels}"

                if line.strip().startswith("nc:"):
                    yaml_lines[i] = f"nc: {len(labels)}"

        latest_data_yaml = "\n".join(yaml_lines)

        with open(working_dir / "data.yaml", "w") as file:
            file.write(latest_data_yaml)

        (working_dir / "runs").mkdir()
        (working_dir / "prelabels").mkdir()

        original_data_dir = working_dir / "original_data"
        original_data_dir.mkdir()  # Create the original_data directory

        labels_folder = original_data_dir / "labels"
        labels_folder.mkdir()  # Create the labels directory

        data_folder = original_data_dir / "images"
        data_folder.mkdir()  # Create the images directory

        if data_dir is not None:
            print("Copying files, please wait...")
            shutil.copytree(data_dir, data_folder, dirs_exist_ok=True)
            print("Files copied successfully.")

        print(f"{working_dir} successfully created!")

        self.current_proj = Path(working_dir)
        return self.current_proj


    def count_data(self, current_proj : str | Path) -> int:
        """
        Stores and returns the total count of data images for the specified project
        Note: will switch the current working project to the one specified

        Args:
            current_proj (str | Path): path to current working project
        
        Raises:
            ValueError if an invalid project directory is provided

        Returns:
            raw count of total images in the directory
        """

        current_proj = Path(current_proj)
        if current_proj is None or not current_proj.is_dir():
            raise ValueError("Invalid project directory")

        count = sum(1 for file in (current_proj).rglob("*") if file.is_file() and file.suffix.lower() in self.SUPPORTED_IMG_EXTENSIONS)

        self.data_num = count
        return count


    def update_findings(self, findings_file : str | Path, contents : str) -> None:
        """
        Updates the findings.txt with contents
        TODO: will be useful for the Evaluator class when updating findings

        Args:
            findings_file (str | Path): path to findings.txt file
            contents (str): contents to write to file

        Returns:
            None 
        """

        with open(findings_file, "w") as file:
            file.write(contents)


    def get_labels_from_config(label_config : str | Path) -> list[str]:
        """
        Extracts labels from the LabelStudio Formatted xml configuration file for classes
        Intended for use inside create_project()

        Args:
            label_config (Path | str) : path to xml config file
        
        Returns: 
            string list of labels
        """
        
        tree = ET.parse(label_config)
        root = tree.getroot()
        labels = [label.get("value") for label in root.iter("Label")]

        return labels


    def _update_cfgs(cfg_dir : Path, yaml_path : Path, working_dir : Path) -> None:
        """
        Updates the yaml configuration files with the correct pathing
        Intended use is for create_project() method

        Args:
            cfg_dir (Path) : path to configuration directory 
            yaml_path (Path) : path to yaml file
            working_dir: path to current working directory

        Returns:
            None
        """

        shutil.copy(yaml_path, cfg_dir)
        cfg_file = Path(cfg_dir) / yaml_path.name
        with open(cfg_file, "r") as f:
            data = yaml.safe_load(f)

        data["data"] = str(working_dir / data["data"])  # adding path to the data : Path/data.yaml
        with open(cfg_file, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)


    def update_yaml_paths(self, current_proj_dir : Path | str) -> None:
        """
        Updates the yaml paths to map to the current directory. This affects
        the data.yaml, args.yaml and tune_args.yaml files respectively
        Intended to be used if the project is renamed at any poing

        Args:
            current_proj_dir (Path | str) : current working project path

        Returns:
            None
        """
        data_yaml = Path(current_proj_dir) / "data.yaml"
        args_yaml = Path(current_proj_dir) / "cfg/args.yaml"
        tune_args_yaml = Path(current_proj_dir) / "cfg/tune_args.yaml"

        with open(data_yaml, "r") as f:
            data = yaml.safe_load(f)
        data["path"] = str(Path(current_proj_dir) / "data")
        with open(data_yaml, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

        with open(args_yaml, "r") as f:
            data = yaml.safe_load(f)
        data["data"] = str(data_yaml)
        with open(args_yaml, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

        with open(tune_args_yaml, "r") as f:
            data = yaml.safe_load(f)
        data["data"] = str(data_yaml)
        with open(tune_args_yaml, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)