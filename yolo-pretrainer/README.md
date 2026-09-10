# Introduction

This is my personal library used to mostly automate the active learning process with yolo

# Class Roles

1 - Creating and managing a project - ProjectManager Class
2 - Training a model - Trainer Class
3 - Evaluating the best model, params, performance - Evaluator Class
4 - Prelabel unlabelled data with that model - PreLabeler
5 - Manually reviewing data - LabelStudioManager
6 - Auto Trainer is the base class that integrates all these classes

# Work flow

The AutoTrainer Class has this workflow:
Note: You must have labelled data manually beforehand and have a currently working model

Create a fresh project <--------------------------------------------
(autotrain.setup_project)                                          |
            |                                                      |
Evaluate best params for given model/data/use case
(autotrain.run(tune=True))
            |                                                      |
Train a model using newly labelled data
(autotrain.update_best_hyperparameters)
(autotrain.run(args_yaml="path to best_yaml"))
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

# Very First Project
1. Setup label studio using the guide if you have not
2. Create a new project using either the Default Label Studio GUI or API in label_studio_manager class
3. If you chose to use the GUI, fill in label studio interface manually or copy paste from the label_config.xml
4. Connect to local storage using the 

2. After labelling is complete, if segmentation export standard json, if box export 'YOLOv8 OBB'
3. Create a project via the project_manager.py method create_project() recommended to set the data_dir parameter to your data path
4. 

# TODO

- Implement Tuner into Trainer class
- Testing pipeline for review via video (Test class?)
- Implement Unit tests for ALL classes
- Prelabeler Review Flagging