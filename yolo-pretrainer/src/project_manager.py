from pathlib import Path

import os
import shutil

class ProjectManager:
    """Class for creating and managing YOLO projects under my custom defined
    project structure 

    @author: Sami Ibrahim
    @version: 8/20/2026

    # Create project with valid directory structure
    # Use file naming scheme and auto increment new project with said scheme
    # Generate findings based on previous version

    Methods:
        __init__: Initiates a project directory (Where projects are stored)
        create_project: creates a new project with pre-defined structure
        update_findings: TODO Update findings with data from Evaluator class
        count_data: counts the amount of data stored for a specific project
    """

    FINDINGS_TEMPLATE = """
    Best Model: 

    Version:

    --------------------------------
    |        Version Updates       |
    --------------------------------
    -


    --------------------------------
    |          Findings            |
    --------------------------------
    - 
    """

    DATA_YAML_TEMPLATE = """
    path:
    train: train\images
    val: val\images

    nc: 3

    names: ["Class1", "Class2", "Class3"]
    """

    PROJECT_TYPE = {
        "seg",
        "box"
    }

    YOLO_VERSION = {
        "yolo26",
        "yolo12",
        "yolo11",
        "yolov10",
        "yolov9",
        "yolov8",
        "yolov7",
        "yolov6",
        "yolov5",
        "yolov4",
        "yolov3"
    }

    def __init__(self, project_dir):
        """
        Initializes the project directory where your projects are stored

        Args:
            project_dir (str | Path): Path to where projects are stored
            data_num (int): total amount of data files for a specific project
            current_proj (str | Path): current working project 

        Returns:
            None
        """
        
        self.project_dir = Path(project_dir)
        self.current_proj = None
        self.data_num = 0
        


    def create_project(self, name=None, data_dir=None, version=None, project_type="box") -> Path:
        """
        Creates a new project within the project directory with my own custom
        pre-defined structure:

        Project Directory --- yolo26_v1.2_box_400 ----- original_data ------ images
                                                     |                       
                                                     |- data.yaml
                                                     |
                                                     |- findings.txt
        
        Note: If a custom name is entered then all other parameters are auto filled
                                                     
        Args:
            name (str): optionally define custom project name
            data_dir (str | Path): directory/location of image data in file system
            version (float): optionally set project version
            project_type (str): define project type, defaults are "seg" or "box"

        Returns:
            Path to project created                                 
        """

        latest_findings = self.FINDINGS_TEMPLATE
        latest_data_yaml = self.DATA_YAML_TEMPLATE

        if name is None:

            if version is None:  # Auto assign version number if none specified
                version = 1.0
                for project in self.project_dir.iterdir():

                    # Checking to see if the project type and version number already exist
                    if project.is_dir() and project.name.find(project_type) != -1:
                        if project.name.find("v" + str(version)) != -1:

                            version = float(version)

                            try:
                                with open(os.path.joing(project, "findings.txt"), "r") as f:
                                    latest_findings = f.read()
                            except FileNotFoundError:
                                print(f"findings.txt not found in {project.name} Skipping...")

                            try:
                                with open(os.path.joing(project, "data.yaml"), "r") as f:
                                    latest_data_yaml = f.read()
                            except FileNotFoundError:
                                print(f"data.yaml not found in {project.name} Skipping...")

                            version += 0.1

            if data_dir is not None and data_dir.is_dir():
                self.count_data(data_dir)  # Updates the attribute data_num
            else:
                self.data_num = 0

            full_name = "yolo26" + "_v" + str(version) + "_" + project_type + "_" + str(self.data_num)
            working_dir = os.path.join(self.project_dir, full_name)

        else:
            working_dir = os.path.join(self.project_dir, name)

        os.mkdir(working_dir)

        findings_path = os.path.join(working_dir, "findings.txt")
        self.update_findings(findings_path, latest_findings)

        with open(os.path.join(working_dir, "data.yaml"), "w") as file:
            file.write(latest_data_yaml)

        original_data_dir = os.path.join(working_dir, "original_data")
        os.mkdir(original_data_dir)

        data_folder = os.path.join(original_data_dir, "data")
        os.mkdir(data_folder)

        if data_dir is not None and data_dir.is_dir():
            shutil.copytree(data_dir, data_folder)



    def count_data(self, current_proj) -> int:
        """
        Stores and returns the total count of data images for the specified project
        Note: will switch the current working project to the one specified

        Args:
            current_proj (str | Path): path to current working project

        Returns:
            raw count of total images in the directory
        """

        if current_proj is None or not current_proj.is_dir():
            current_proj = self.create_project()
        else:
            self.current_proj = current_proj

        count = 0
        for project in current_proj.rglob("*"):
            count += 1

        self.data_num = count
        return count



    def update_findings(self, findings_file, contents):
        """
        Updates the findings file with contents
        TODO: will be useful for the Evaluator class when updating findings

        Args:
            findings_file (str | Path): path to findings.txt file
            contents (str): contents to write to file

        Returns:
            None 
        """
        try:
            with open(findings_file, "w") as file:
                file.write(contents)
        except FileNotFoundError:
            print("File does not exist")