from src.trainer import Trainer
from src.config import (CURRENT_WORKING_PROJECT_DIRECTORY, ARGS_YAML_CONFIG, RESUME_MODEL)

"""
Begins model training using the current projects args.yaml configuration file
resume functionality is present within the trainer class if desired

Requires:
    CURRENT_WORKING_PROJECT_DIRECTORY
    ARGS_YAML_CONFIG

Optional:
    RESUME_MODEL
"""

def main():
    trainer = Trainer()
    trainer.train(cfg=ARGS_YAML_CONFIG, current_proj_dir=CURRENT_WORKING_PROJECT_DIRECTORY, resume=RESUME_MODEL)

if __name__ == "__main__":
    main()