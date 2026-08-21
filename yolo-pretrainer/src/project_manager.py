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

    DATA_YAML_TEMPLATE = """path:
train: train\images
val: val\images

nc: 3

names: ["Class1", "Class2", "Class3"]"""

    SUPPORTED_IMG_EXTENSIONS = {
        ".jpg", 
        ".jpeg", 
        ".png"
    }

    SUPPORTED_PROJECT_TYPES = {"box", "seg"}
    
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
        
        Raises:
            ValueError if project_type is not supported
            FileExistsError if the project already exists
        
        Returns:
            Path to project created                                 
        """

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
                            curr_version = float(parts[1][1:])

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

            full_name = "yolo26" + "_v" + str(version) + "_" + project_type + "_" + str(self.data_num)
            working_dir = self.project_dir / full_name

        else:
            working_dir = self.project_dir / name

        if working_dir.exists():
            raise FileExistsError(f"Error {working_dir} already exists")
        working_dir.mkdir()

        findings_path = working_dir / "findings.txt"
        self.update_findings(findings_path, latest_findings)


        # data.yaml path overwrite
        yaml_lines = latest_data_yaml.splitlines()
        for i, line in enumerate(yaml_lines):
            if line.strip().startswith("path:"):
                yaml_lines[i] = f"path: {working_dir}\data"
                break
        latest_data_yaml = "\n".join(yaml_lines)

        with open(working_dir / "data.yaml", "w") as file:
            file.write(latest_data_yaml)

        original_data_dir = working_dir / "original_data"
        original_data_dir.mkdir()

        data_folder = original_data_dir / "data"
        data_folder.mkdir()

        if data_dir is not None:
            shutil.copytree(data_dir, data_folder, dirs_exist_ok=True)

        print(f"{working_dir} successfully created!")

        self.current_proj = Path(working_dir)
        return self.current_proj



    def count_data(self, current_proj) -> int:
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

        count = sum(1 for file in current_proj.rglob("*") if file.is_file() and file.suffix.lower() in self.SUPPORTED_IMG_EXTENSIONS)

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

        with open(findings_file, "w") as file:
            file.write(contents)