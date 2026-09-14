# Introduction

This is my personal library used to mostly automate the active learning process with yolo


# Layout

data/  
    images/ <- image data is stored her
docs/
    YOLO Terminology Guide.txt  <- List of useful terminology in my own words
projects/  <- Here is where my yolo training runs exist (model .pt file + statistics)
scripts/
    label_studio_launch.py  <- Launches Label Studio
    label_studio_setup_project.py  <- Sets up a new project in label studio using the API
    prelabel.py  <- Generates prediction labels for the images of your choice
    setup_project.py <- This script generates and sets up a new Project
    train.py  <- Begins model training using the current projects args.yaml configuration file
    tune.py <- Begins model tuning using the current projects tune_args.yaml configuration file
src/
    cfg/
        args.yaml <- contains template arguments for training a model
        tune_args.yaml <- contains template arguments for hyperparameter tuning
        label_config_seg <- contains the segmentaton labelling classes for Label Studio
        label_config_box <- contains the OBB (boxes) labelling classes for Label Studio
    utils/
        brush.py  <- Label studio adapter tools from https://github.com/HumanSignal/label-studio-converter
        ml_stratifiers <- training data split methods adapted from https://github.com/trent-b/iterative-stratification
    config.py  <- central configuration for the script files and classes
    project_manager.py <- class for creating and managing YOLO projects under my custom defined project structure 
    label_studio_manager.py <- class containing optional utilities for interfacing with label studio
    trainer.py <- class containing YOLO methods for optimized training & tuning of models
    prelabeler.py <- class for prelabelling image datasets using YOLO models
    auto_trainer.py <- Manager class where all class methods are combined to automate the full YOLO active learning pipeline
    evaluator.py (INCOMPLETE) <- class to provide both qualitative and quantitative analysis of model performance for clients
tests/
    standard tests for all classes: test_prelabeler.py
label-studio.bat <- bat file for launching label studio (please edit the executable path using a text editor e.g. notepad)


# One-time setup
pip install -r requirements.txt

# Data Pipeline

# (optional) create a new .env file in the base directory (the borescope-yolo-training/) with
API_KEY="Fill In API key here"
LABEL_STUDIO_PATH="Fill in path to exe here"

# 1. setting up a new project
In src/config.py fill in: BASE_DIRECTORY, LABELS_JSON_FILE
python -m scripts.setup_project

# 2. begin training run
In src/config.py fill in: CURRENT_WORKING_PROJECT_DIRECTORY
If desired edit arguments in your project /cfg/args.yaml
python -m scripts.train

# (optional) tuning a model
In src/config.py fill in: UPDATE_ARGS_YAML_WITH_TUNED_ONES, CURRENT_WORKING_PROJECT_DIRECTORY
If desired edit arguments in your project /cfg/tune_args.yaml
python -m scripts.tune

# 3. run the model live (Non-InspectStudio)
In src/config.py fill in: MODEL_FOR_PREDICTIONS, MIN_CONF, MAX_CONF, LIVE_FEED
python -m scripts.run_live

# 4. generate Label Studio predictions using the model
In src/config.py fill in: MODEL_FOR_PREDICTIONS, MIN_CONF, MAX_CONF, IMAGES_TO_PREDICT
python -m scripts.prelabel


# Class Roles

1 - Creating and managing a project - ProjectManager Class
2 - Training a model - Trainer Class
3 - Evaluating the best model, params, performance - Evaluator Class (INCOMPLETE)
4 - Prelabel unlabelled data with that model - PreLabeler
5 - Manually labelling & reviewing data - LabelStudioManager
6 - Auto Trainer is the base class that integrates all these classes - AutoTrainer

# Work flow

The AutoTrainer Class has this workflow:
Note: You must have labelled data manually beforehand and have a currently working model

Create a fresh project <--------------------------------------------
setup                                          |
            |                                                      |
Evaluate best params for given model/data/use case
(INCOMPLETE)
            |                                                      |
Train a model using newly labelled data
            |                                                      |
Evaluate generated statistics with report
            |                                                      |
Prelabel unlabelled data with new model
            |                                                      |
Manually review and fix newly annotated data
            |                                                      |
Retrain until satisfied --------------------------------------------


# Getting Started

## Label Studio Setup Guide ##
Download Label studio using the following guide https://labelstud.io/guide/install.html#Install-using-pip 
Make sure to edit the label-studio.bat file label studio directory path (the default is "C:\labelstudioenv\Scripts")

- setting up local storage
-- editing the bat file --
set the LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT to one folder before the actual image folder
e.g. if your data is in C:/projects/data/images/  set it to C:\\projects\\data  (use '\\' as label studio is sensitive)

Create a project -> Open project Settings -> Cloud Storage -> Add Source Storage -> Local Files -> Add e.g.  C:\\projects\\data\\images --> Test connection -> Change import method from 'Tasks' to 'Files' 

WARNING: If you are importing json labels DO NOT click 'Save & Sync' or duplicates will be created upon pressing this, just press "Save" then import your json labels and everything will work as intended. If you just want to start fresh without importing prelabels 'Save & Sync' works fine

Default Labelling interface can be found in borescope-yolo-training/src/cfg/label_config.xml, just copy paste it in the label studio Labelling Interface tab and click save

Using the label_studio_manager.py class requires an API key. This can be found in Account & Settings -> Personal Access Token
You may paste this in a fresh .env file (just create one and add the)

A useful feature of label studio is that if you are just importing labels. You don't have to edit the original data size.
So if I have something like 20 image dataset, and label 5 of those images export a json. If I were to import that json file
and the data directory is set to the location of the 20 image dataset, it will just import 5 of those images instead of having to manually filter everything yourself.

Import an old project use the label_studio_setup_project.py script
run python -m scripts.label_studio_setup_project

# Very First Project
1. Setup label studio using the guide if you have not
2. Create a new project using either the Default Label Studio GUI or API in label_studio_manager class
3. If you chose to use the GUI, fill in label studio interface manually or copy paste from the label_config.xml
4. Connect to local storage using the 

2. After labelling is complete, if segmentation export standard json, if box export 'YOLOv8 OBB'
3. Create a project via the project_manager.py method create_project() recommended to set the data_dir parameter to your data path


# TODO

- Implement Tuner into Trainer class
- Testing pipeline for review via video (Test class?)
- Implement Unit tests for ALL classes
- Prelabeler Review Flagging