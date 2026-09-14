# YOLO Active Learning Automation

## Introduction

This project is a personal library designed to automate much of the YOLO active learning workflow. It provides tools for:

- Managing YOLO training projects
- Integrating with Label Studio
- Generating prelabels using trained models
- Training and hyperparameter tuning
- Automating iterative active learning pipelines

The goal is to reduce manual effort when creating, labeling, training, and improving YOLO datasets and models.

---

# Features

- Label Studio integration
- Automated project creation and management
- YOLO model training
- Hyperparameter tuning
- Automatic prelabel generation
- Active learning workflow automation
- Live model inference
- Dataset management utilities
- Unit testing support

---

# Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

---

# Label Studio Setup

## 1. Install Label Studio

Follow the official installation guide:

https://labelstud.io/guide/install.html#Install-using-pip

---

## 2. Configure `label-studio.bat`

Open `label-studio.bat` with a text editor and update the Label Studio executable path.

Example:

```text
C:\labelstudioenv\Scripts
```

---

## 3. Configure Local Storage

Set:

```text
LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT
```

to the directory **one level above** your image folder.

Example:

Dataset location:

```text
C:\projects\data\images
```

Configuration:

```text
C:\projects\data
```

**Important:** Use double backslashes (`\\`) as Label Studio can be sensitive to path formatting.

---

## 4. Connect Local Storage

Within Label Studio:

1. Create a project
2. Open **Project Settings**
3. Navigate to **Cloud Storage**
4. Select **Add Source Storage**
5. Choose **Local Files**
6. Provide your image folder path

Example:

```text
C:\projects\data\images
```

7. Click **Test Connection**
8. Change Import Method from:

```text
Tasks
```

to

```text
Files
```

9. Save

---

## Importing Existing Labels

### Warning

If you are importing JSON annotations:

**Do not click "Save & Sync".**

Doing so can create duplicate tasks.

Instead:

1. Click **Save**
2. Import your JSON annotations
3. Continue working normally

If you are starting a completely new project without importing labels, using **Save & Sync** is fine.

---

## Labeling Interface

Default labeling interfaces are provided in:

### Segmentation

```text
src/cfg/label_config_seg.xml
```

### OBB / Bounding Boxes

```text
src/cfg/label_config_box.xml
```

Copy the contents into the Label Studio **Labeling Interface** editor and save.

---

## API Key Configuration

`LabelStudioManager` requires a Label Studio Personal Access Token.

You can generate one from:

```text
Account & Settings -> Personal Access Token
```

Create a `.env` file in the project root:

```env
API_KEY="your_api_key_here"
LABEL_STUDIO_PATH="path_to_label_studio_executable"
```

Example:

```env
API_KEY="abc123"
LABEL_STUDIO_PATH="C:\labelstudioenv\Scripts\label-studio.exe"
```

---

## Helpful Label Studio Behavior

Label Studio only imports images referenced by the annotation file.

Example:

- Dataset contains 20 images
- JSON contains labels for 5 images

When importing the JSON, Label Studio automatically loads only those 5 images. There is no need to manually create a filtered dataset.

---

# Quick Start

## Launch Label Studio

```bash
python -m scripts.label_studio_launch
```

## Import an Existing Project

Ensure Label Studio is already running:

```bash
python -m scripts.label_studio_setup_project
```

---

## Creating Your First Project

1. Complete the Label Studio setup above.
2. Create a new Label Studio project.
3. Configure the labeling interface manually or using one of the provided XML files.
4. Label some data.

When exporting annotations:

- Segmentation projects → **JSON**
- OBB projects → **YOLOv8 OBB**

---

# Project Structure

```text
data/
└── images/

docs/
└── YOLO Terminology Guide.txt

projects/
└── YOLO training projects

scripts/
├── label_studio_launch.py
├── label_studio_setup_project.py
├── prelabel.py
├── setup_project.py
├── train.py
├── tune.py
└── run_live.py

src/
├── cfg/
│   ├── args.yaml
│   ├── tune_args.yaml
│   ├── label_config_seg.xml
│   └── label_config_box.xml
│
├── utils/
│   ├── brush.py
│   └── ml_stratifiers/
│
├── config.py
├── project_manager.py
├── label_studio_manager.py
├── trainer.py
├── prelabeler.py
├── auto_trainer.py
└── evaluator.py

tests/
└── test_*.py

label-studio.bat
```

---

# Workflow

The active learning cycle implemented by `AutoTrainer` is:

```text
Create Project
      │
      ▼
Train Model
      │
      ▼
Generate Prelabels
      │
      ▼
Manually Review Labels
      │
      ▼
Retrain Model
      │
      ▼
Satisfied?
  ├─ No ─────────────┐
  │                  │
  └──── Repeat ◄─────┘
```

### Requirements

Before starting:

- A manually labeled dataset must already exist.
- A baseline model must already be available.

---

# Main Classes

## ProjectManager

Responsible for:

- Project creation
- Dataset management
- Configuration management

## Trainer

Responsible for:

- Model training
- Hyperparameter tuning
- Training result management

## LabelStudioManager

Responsible for:

- Label Studio API integration
- Project setup automation
- Label Studio utility functions

## PreLabeler

Responsible for:

- Running YOLO predictions
- Generating labels for unlabeled data

## Evaluator *(Work In Progress)*

Planned functionality:

- Quantitative model evaluation
- Qualitative model review
- Client-facing performance reporting

## AutoTrainer

The central orchestration class that combines all project components into a complete active learning pipeline.

---

# Training Pipeline

## 1. Create a New Project

Update the following values in `src/config.py`:

```python
BASE_DIRECTORY
LABELS_JSON_FILE
```

Run:

```bash
python -m scripts.setup_project
```

---

## 2. Train a Model

Update:

```python
CURRENT_WORKING_PROJECT_DIRECTORY
```

Optionally edit:

```text
project/cfg/args.yaml
```

Run:

```bash
python -m scripts.train
```

---

## 3. Hyperparameter Tuning (Optional)

Update:

```python
UPDATE_ARGS_YAML_WITH_TUNED_ONES
CURRENT_WORKING_PROJECT_DIRECTORY
```

Optionally edit:

```text
project/cfg/tune_args.yaml
```

Run:

```bash
python -m scripts.tune
```

---

## 4. Run Live Inference

Update:

```python
MODEL_FOR_PREDICTIONS
MIN_CONF
MAX_CONF
LIVE_FEED
```

Run:

```bash
python -m scripts.run_live
```

---

## 5. Generate Prelabels

Update:

```python
MODEL_FOR_PREDICTIONS
MIN_CONF
MAX_CONF
IMAGES_TO_PREDICT
```

Run:

```bash
python -m scripts.prelabel
```

---

# Testing

Run all tests:

```bash
python -m pytest
```

---

# Acknowledgements

The following utilities are adapted from existing open-source projects:

- Label Studio Converter: https://github.com/HumanSignal/label-studio-converter
- Iterative Stratification: https://github.com/trent-b/iterative-stratification

---

# TODO

- [ ] Prelabel review flagging
- [ ] Complete evaluator implementation
- [ ] Improve automated active learning reporting