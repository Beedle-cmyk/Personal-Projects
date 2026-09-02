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
            |                                                      |
Evaluate best params for given model/data/use case
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

# TODO

- Implement Tuner into Trainer class
- Testing pipeline for review via video (Test class?)
- Implement Unit tests for ALL classes
- Prelabeler Review Flagging