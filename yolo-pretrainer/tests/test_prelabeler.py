# tests/test_prelabeler.py

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import torch

from src.prelabeler import Prelabeler


# ============================================================
# helpers
# ============================================================

class MockBox:
    def __init__(self, cls_id, conf, xyxy):
        self.cls = [cls_id]
        self.conf = [conf]
        self.xyxy = [torch.tensor(xyxy)]


# ============================================================
# __init__ / model initialization
# ============================================================

@patch.object(Prelabeler, "_initialize_model")
def test_init(mock_init):
    mock_model = MagicMock()
    mock_init.return_value = mock_model

    p = Prelabeler(
        model_path="model.pt",
        min_conf=0.1,
        max_conf=0.9,
        image_dir="images"
    )

    assert p.model == mock_model
    assert p.min_conf == 0.1
    assert p.max_conf == 0.9
    assert p.image_dir == Path("images")


@patch("src.prelabeler.YOLO")
def test_initialize_model_pt(mock_yolo):
    p = Prelabeler.__new__(Prelabeler)

    model = p._initialize_model("best.pt")

    mock_yolo.assert_called_once()
    assert model == mock_yolo.return_value


def test_initialize_model_none():
    p = Prelabeler.__new__(Prelabeler)

    with pytest.raises(ValueError):
        p._initialize_model(None)


def test_initialize_model_invalid_extension():
    p = Prelabeler.__new__(Prelabeler)

    with pytest.raises(ValueError):
        p._initialize_model("model.onnx")


# ============================================================
# set_confidence
# ============================================================

def test_set_confidence():
    p = Prelabeler.__new__(Prelabeler)

    p.set_confidence(0.2, 0.8)

    assert p.min_conf == 0.2
    assert p.max_conf == 0.8


@pytest.mark.parametrize(
    "min_conf,max_conf",
    [
        (-0.1, 0.8),
        (0.2, 1.1),
        (5, 6),
    ],
)
def test_set_confidence_invalid(min_conf, max_conf):
    p = Prelabeler.__new__(Prelabeler)

    with pytest.raises(ValueError):
        p.set_confidence(min_conf, max_conf)


# ============================================================
# box_iou
# ============================================================

def test_box_iou_identical():
    box = [0, 0, 100, 100]

    assert Prelabeler.box_iou(box, box) == pytest.approx(1.0)


def test_box_iou_no_overlap():
    box1 = [0, 0, 10, 10]
    box2 = [20, 20, 30, 30]

    assert Prelabeler.box_iou(box1, box2) == 0.0


def test_box_iou_partial_overlap():
    box1 = [0, 0, 100, 100]
    box2 = [50, 50, 150, 150]

    iou = Prelabeler.box_iou(box1, box2)

    assert 0 < iou < 1


# ============================================================
# mask_overlap
# ============================================================

def test_mask_overlap_identical():
    mask = torch.tensor(
        [
            [0, 1],
            [1, 1]
        ]
    )

    overlap = Prelabeler.mask_overlap(mask, mask)

    assert overlap == pytest.approx(1.0)


def test_mask_overlap_none():
    mask1 = torch.tensor(
        [
            [1, 0],
            [0, 0]
        ]
    )

    mask2 = torch.tensor(
        [
            [0, 0],
            [0, 1]
        ]
    )

    assert Prelabeler.mask_overlap(mask1, mask2) == 0.0


def test_mask_overlap_empty_masks():
    mask1 = torch.zeros((4, 4))
    mask2 = torch.zeros((4, 4))

    assert Prelabeler.mask_overlap(mask1, mask2) == 0.0


# ============================================================
# check_overlap
# ============================================================

def test_check_overlap_detected():
    mask = torch.tensor(
        [
            [1, 1],
            [1, 1]
        ]
    )

    boxes = [
        MockBox(0, 0.9, [0, 0, 100, 100]),
        MockBox(0, 0.8, [0, 0, 100, 100]),
    ]

    detected = Prelabeler.check_overlap(
        [mask, mask],
        boxes,
        overlap_threshold=0.8,
    )

    assert detected is True


def test_check_overlap_different_classes():
    mask = torch.ones((2, 2))

    boxes = [
        MockBox(0, 0.9, [0, 0, 100, 100]),
        MockBox(1, 0.8, [0, 0, 100, 100]),
    ]

    assert (
        Prelabeler.check_overlap(
            [mask, mask],
            boxes,
            overlap_threshold=0.8,
        )
        is False
    )


# ============================================================
# same_prediction
# ============================================================

def test_same_prediction_empty():
    assert Prelabeler.same_prediction([], []) is True


def test_same_prediction_different_count():
    a = [MockBox(0, 0.9, [0, 0, 10, 10])]

    assert Prelabeler.same_prediction(a, []) is False


def test_same_prediction_different_class():
    a = [MockBox(0, 0.9, [0, 0, 10, 10])]
    b = [MockBox(1, 0.9, [0, 0, 10, 10])]

    assert Prelabeler.same_prediction(a, b) is False


def test_same_prediction_same_boxes():
    a = [MockBox(0, 0.9, [0, 0, 100, 100])]
    b = [MockBox(0, 0.8, [0, 0, 100, 100])]

    assert Prelabeler.same_prediction(a, b) is True


def test_same_prediction_low_iou():
    a = [MockBox(0, 0.9, [0, 0, 50, 50])]
    b = [MockBox(0, 0.9, [80, 80, 120, 120])]

    assert Prelabeler.same_prediction(a, b) is False


# ============================================================
# box_predict
# ============================================================

@patch.object(Prelabeler, "_initialize_model")
def test_box_predict_generates_json(mock_init, tmp_path):
    image_dir = tmp_path / "images"
    image_dir.mkdir()

    (image_dir / "img1.jpg").touch()

    model = MagicMock()

    box = MockBox(
        cls_id=0,
        conf=0.95,
        xyxy=[10, 20, 100, 200]
    )

    prediction = MagicMock()
    prediction.orig_shape = (500, 500)
    prediction.boxes = [box]

    model.return_value = [prediction]
    model.names = {0: "staining"}

    mock_init.return_value = model

    p = Prelabeler(
        "model.pt",
        0.0,
        1.0,
        image_dir=image_dir,
        output_dir=tmp_path,
    )

    p.box_predict()

    output = tmp_path / "box_predictions.json"

    assert output.exists()

    data = json.loads(output.read_text())

    assert len(data) == 1
    assert data[0]["predictions"][0]["result"]


# ============================================================
# seg_predict
# ============================================================

@patch("src.prelabeler.LabelStudioManager.ls_convert")
@patch.object(Prelabeler, "_initialize_model")
def test_seg_predict_generates_json(
    mock_init,
    mock_rle,
    tmp_path,
):
    image_dir = tmp_path / "images"
    image_dir.mkdir()

    (image_dir / "img1.jpg").touch()

    mask = torch.ones((10, 10))

    box = MockBox(
        cls_id=0,
        conf=0.95,
        xyxy=[0, 0, 100, 100],
    )

    prediction = MagicMock()
    prediction.orig_shape = (100, 100)

    prediction.masks = MagicMock()
    prediction.masks.data = [mask]
    prediction.boxes = [box]

    model = MagicMock()
    model.return_value = [prediction]
    model.names = {0: "staining"}

    mock_rle.return_value = [1, 2, 3]

    mock_init.return_value = model

    p = Prelabeler(
        "model.pt",
        0.0,
        1.0,
        image_dir=image_dir,
        output_dir=tmp_path,
    )

    p.seg_predict()

    output = tmp_path / "seg_predictions.json"

    assert output.exists()

    data = json.loads(output.read_text())

    assert len(data) == 1
    assert len(data[0]["predictions"][0]["result"]) == 1


# ============================================================
# supported image extensions
# ============================================================

def test_supported_extensions():
    assert ".jpg" in Prelabeler.SUPPORTED_IMG_EXTENSIONS
    assert ".jpeg" in Prelabeler.SUPPORTED_IMG_EXTENSIONS
    assert ".png" in Prelabeler.SUPPORTED_IMG_EXTENSIONS