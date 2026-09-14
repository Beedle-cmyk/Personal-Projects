import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import torch
import yaml

from src.label_studio_manager import LabelStudioManager


# ============================================================
# mapping_class
# ============================================================

def test_mapping_class():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }

    assert (
        LabelStudioManager.mapping_class(
            "dog",
            mapping,
        ) == 1
    )


def test_mapping_class_missing():
    mapping = {
        0: "cat",
    }

    with pytest.raises(ValueError):
        LabelStudioManager.mapping_class(
            "horse",
            mapping,
        )


# ============================================================
# polygon_to_yolo
# ============================================================

def test_polygon_to_yolo():
    points = [
        (50, 25),
        (100, 0),
    ]

    result = LabelStudioManager.polygon_to_yolo(
        points
    )

    assert result == [
        0.5,
        0.25,
        1.0,
        0.0,
    ]


def test_polygon_to_yolo_empty():
    assert (
        LabelStudioManager.polygon_to_yolo([])
        == []
    )


# ============================================================
# _load_labels_mapping
# ============================================================

def test_load_labels_mapping(tmp_path):
    yaml_file = tmp_path / "data.yaml"

    yaml_file.write_text(
        yaml.dump(
            {
                "names": [
                    "cat",
                    "dog",
                ]
            }
        )
    )

    mapping = LabelStudioManager._load_labels_mapping(
        tmp_path
    )

    assert mapping == {
        0: "cat",
        1: "dog",
    }


# ============================================================
# ls_convert
# ============================================================

@patch("src.label_studio_manager.brush.mask2rle")
def test_ls_convert(mock_mask2rle):
    mask = torch.tensor(
        [
            [0.0, 1.0],
            [1.0, 0.0],
        ]
    )

    mock_mask2rle.return_value = [1, 2, 3]

    result = LabelStudioManager.ls_convert(
        mask,
        width=2,
        height=2,
    )

    assert result == [1, 2, 3]

    mock_mask2rle.assert_called_once()


# ============================================================
# create_project
# ============================================================

def test_create_project():
    manager = LabelStudioManager.__new__(
        LabelStudioManager
    )

    project = MagicMock()
    project.id = 123

    manager.client = MagicMock()
    manager.client.projects.create.return_value = project

    result = manager.create_project(
        "Test Project",
        "<View></View>",
    )

    assert result == 123
    assert manager.project_id == 123


# ============================================================
# import_json
# ============================================================

def test_import_json(tmp_path):
    manager = LabelStudioManager.__new__(
        LabelStudioManager
    )

    manager.project_id = 10
    manager.client = MagicMock()

    json_file = tmp_path / "tasks.json"

    json_file.write_text(
        json.dumps(
            [{"data": {"image": "img.jpg"}}]
        )
    )

    manager.import_json(
        None,
        json_file,
    )

    manager.client.projects.import_tasks.assert_called_once()


def test_import_json_requires_project():
    manager = LabelStudioManager.__new__(
        LabelStudioManager
    )

    manager.project_id = None

    with pytest.raises(ValueError):
        manager.import_json(
            None,
            "tasks.json",
        )


# ============================================================
# launch
# ============================================================

@patch("src.label_studio_manager.subprocess.Popen")
def test_launch(mock_popen):
    manager = LabelStudioManager.__new__(
        LabelStudioManager
    )

    manager.data_dir = "C:/data"
    manager.ls_path = "C:/labelstudio"

    manager.launch()

    mock_popen.assert_called_once()


# ============================================================
# terminate
# ============================================================

def test_terminate():
    manager = LabelStudioManager.__new__(
        LabelStudioManager
    )

    process = MagicMock()

    manager.process = process

    manager.terminate()

    process.terminate.assert_called_once()
    process.wait.assert_called_once()


# ============================================================
# seg_json_to_yolo
# ============================================================

@patch.object(
    LabelStudioManager,
    "_load_labels_mapping"
)
@patch.object(
    LabelStudioManager,
    "polygon_to_yolo"
)
def test_seg_json_to_yolo_polygon(
    mock_polygon,
    mock_mapping,
    tmp_path,
):
    mock_mapping.return_value = {
        0: "cat"
    }

    mock_polygon.return_value = [
        0.1,
        0.1,
        0.5,
        0.5,
        0.7,
        0.7,
    ]

    export_json = tmp_path / "export.json"

    export_json.write_text(
        json.dumps(
            [
                {
                    "data": {
                        "image": "img1.jpg"
                    },
                    "annotations": [
                        {
                            "result": [
                                {
                                    "type": "polygonlabels",
                                    "value": {
                                        "polygonlabels": [
                                            "cat"
                                        ],
                                        "points": [
                                            [10, 10],
                                            [50, 50],
                                            [70, 70]
                                        ],
                                    },
                                    "original_height": 100,
                                    "original_width": 100,
                                }
                            ]
                        }
                    ]
                }
            ]
        )
    )

    output_dir = tmp_path / "labels"
    output_dir.mkdir()

    LabelStudioManager.seg_json_to_yolo(
        export_json,
        tmp_path,
        output_dir,
    )

    output_file = output_dir / "img1.txt"

    assert output_file.exists()

    contents = output_file.read_text()

    assert contents.startswith("0 ")


# ============================================================
# skipped cancelled annotations
# ============================================================

@patch.object(
    LabelStudioManager,
    "_load_labels_mapping"
)
def test_seg_json_skips_cancelled(
    mock_mapping,
    tmp_path,
):
    mock_mapping.return_value = {
        0: "cat"
    }

    export_json = tmp_path / "export.json"

    export_json.write_text(
        json.dumps(
            [
                {
                    "data": {
                        "image": "img1.jpg"
                    },
                    "annotations": [
                        {
                            "was_cancelled": True,
                            "result": []
                        }
                    ]
                }
            ]
        )
    )

    output_dir = tmp_path / "labels"
    output_dir.mkdir()

    LabelStudioManager.seg_json_to_yolo(
        export_json,
        tmp_path,
        output_dir,
    )

    assert not list(
        output_dir.glob("*.txt")
    )