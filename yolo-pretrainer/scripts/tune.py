from auto_trainer import AutoTrainer
from config import (PROJECT_DIRECTORY, DATA_DIRECTORY, CURRENT_WORKING_PROJECT_DIRECTORY, UPDATE_ARGS_YAML_WITH_TUNED_ONES)

"""
Begins model tuning using the current projects tune_args.yaml configuration file

Requires:
    PROJECT_DIRECTORY
    DATA_DIRECTORY
    CURRENT_WORKING_PROJECT_DIRECTORY

Optional: 
    UPDATE_ARGS_YAML_WITH_TUNED_ONES
"""

auto_trainer = AutoTrainer(proj_dir=PROJECT_DIRECTORY, data_dir=DATA_DIRECTORY)
auto_trainer.run(current_proj_dir=CURRENT_WORKING_PROJECT_DIRECTORY, tune=True)
if UPDATE_ARGS_YAML_WITH_TUNED_ONES: auto_trainer.update_best_hyperparameters(CURRENT_WORKING_PROJECT_DIRECTORY)