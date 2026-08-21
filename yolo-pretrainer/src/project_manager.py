from pathlib import Path

import os

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
            project_dir: Path to where projects are stored
            yolo_version: chosen yolo version
            data_num : total amount of data files for a specific project 

        Returns:
            None
        """
        
        self.project_dir = Path(project_dir)
        self.yolo_version = None
        self.data_num = 0
        


    def create_project(self, name=None, data_dir=None, version=None, project_type="box") -> Path:
        """
        Creates a new project within the project directory with my own custom
        pre-defined structure:

        Project Directory --- yolo26_v1.2_box_400 ----- original_data ------ images
                                                     |                     |
                                                     |                     - labels
                                                     |
                                                     |- data.yaml
                                                     |
                                                     |- findings.txt
        
        Args:
            name (str): optionally define custom project name
            data_dir (str | Path): directory/location of image data in file system
            version (float): optionally set project version
            project_type (str): define project type, defaults are "seg" or "box"

        Returns:
            Path to project created                                 
        """

        if name is None:
            # Auto assign version number if none specified
            if version is None:
                version = 1.0
                for project in self.project_dir.iterdir():
                    if project.is_dir() and project.name.find(project_type) != -1:

                        version_index = project.name.find("v" + str(version))
                        if version_index != -1:
                            version = float(version)
                            # try:
                            #     with open(os.path.joing(project, "findings.txt")) as f:
                            # except FileNotFoundError:
                        version += 0.1

            full_name = "yolo26" + "_v" + str(version) + "_" + project_type + "_" + data_dir data number
            working_dir = os.path.join(self.project_dir, full_name)

        else:
            working_dir = os.path.join(self.project_dir, name)
            os.mkdir(working_dir)

        with open("findings.txt") as file:
            file.write(self.FINDINGS_TEMPLATE)

    def count_data(self, project_name):
