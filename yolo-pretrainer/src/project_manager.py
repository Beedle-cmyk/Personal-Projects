from pathlib import Path

import os

class ProjectManager:
    """Class for managing projects

    @author: Sami Ibrahim
    @version: 8/20/2026

    # Create project with valid directory structure
    # Use file naming scheme and auto increment new project with said scheme
    # Generate findings based on previous version
    # stratified split to split the data ?? or should be in trainer?

    Methods:
        __init__:
        create_project:
        
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

    def __init__(self, project_dir):
        """
        """
        
        self.project_dir = Path(project_dir)



    def create_project(self, name=None, data_dir=None, version=None, project_type="box"):
        """
        Creates a new project within the project directory
        Will
        """
        if name is None:
            if version is None:
                version = 1.0
                for dir_name in self.project_dir:
                    if dir_name.contains(str(version)):
                        version = float(version)
                        try:
                            with open(dir_name + "/findings.txt") as f:
                                
                        except:
                            pass
                version += 0.1

            full_name = "yolo26" + "_v" + str(version) + "_" + project_type + "_" + data_dir data number
            working_dir = os.path.join(self.project_dirm, full_name)

        else:
            working_dir = os.path.join(self.project_dir, name)
            os.mkdir(working_dir)


        with open("findings.txt") as file:
            file.write(self.FINDINGS_TEMPLATE)
        