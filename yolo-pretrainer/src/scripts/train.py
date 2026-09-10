from auto_trainer import AutoTrainer
from config import (PROJECT_DIRECTORY, DATA_DIRECTORY, CURRENT_WORKING_PROJECT_DIRECTORY)

"""
Begins model training using the current projects args.yaml configuration file

Requires:
    PROJECT_DIRECTORY
    DATA_DIRECTORY
    CURRENT_WORKING_PROJECT_DIRECTORY
"""

auto_trainer = AutoTrainer(proj_dir=PROJECT_DIRECTORY, data_dir=DATA_DIRECTORY)
auto_trainer.run(current_proj_dir=CURRENT_WORKING_PROJECT_DIRECTORY)