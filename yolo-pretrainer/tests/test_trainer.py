from collections import Counter
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from src.trainer import Trainer


# ============================================================
# __init__
# ============================================================

def test_init_sets_default_attributes():
    trainer = Trainer()

    assert trainer.model is None
    assert trainer.latest_results is None
    assert trainer.run_name is None


# ============================================================
# validate_cuda
# ============================================================

@patch("torch.cuda.is_available", return_value=True)
@patch("torch.cuda.get_device_name", return_value="RTX 4090")
def test_validate_cuda_gpu(mock_name, mock_available, capsys):
    Trainer.validate_cuda()

    output = capsys.readouterr().out

    assert "GPU detected" in output


@patch("builtins.input", return_value="y")
@patch("torch.cuda.is_available", return_value=False)
def test_validate_cuda_cpu_continue(mock_cuda, mock_input, capsys):
    Trainer.validate_cuda()

    output = capsys.readouterr().out

    assert "CUDA is not available" in output


@patch("builtins.input", return_value="n")
@patch("torch.cuda.is_available", return_value=False)
def test_validate_cuda_cpu_cancel(mock_cuda, mock_input):
    with pytest.raises(SystemExit):
        Trainer.validate_cuda()


# ============================================================
# train / tune wrappers
# ============================================================

def test_train_calls_run():
    trainer = Trainer()

    with patch.object(trainer, "_run", return_value="result") as mock_run:
        result = trainer.train()

    assert result == "result"

    mock_run.assert_called_once_with(
        cfg="args.yaml",
        current_proj_dir=None,
        tune=False,
        resume=None
    )


def test_tune_calls_run():
    trainer = Trainer()

    with patch.object(trainer, "_run", return_value="result") as mock_run:
        result = trainer.tune()

    assert result == "result"

    mock_run.assert_called_once_with(
        cfg="args.yaml",
        current_proj_dir=None,
        tune=True
    )


# ============================================================
# _run
# ============================================================

@patch("src.trainer.Trainer.validate_cuda")
@patch("src.trainer.YOLO")
def test_run_raises_when_model_missing(
    mock_yolo,
    mock_validate,
    tmp_path,
):
    cfg = tmp_path / "args.yaml"

    cfg.write_text(
        yaml.dump(
            {
                "imgsz": 640,
                "epochs": 100,
            }
        )
    )

    trainer = Trainer()

    with pytest.raises(ValueError):
        trainer._run(cfg)


@patch("src.trainer.Trainer.validate_cuda")
@patch("src.trainer.YOLO")
def test_run_train_success(
    mock_yolo_class,
    mock_validate,
    tmp_path,
):
    cfg = tmp_path / "args.yaml"

    cfg.write_text(
        yaml.dump(
            {
                "model": "yolo11n.pt",
                "imgsz": 640,
                "epochs": 100,
            }
        )
    )

    mock_model = MagicMock()
    mock_model.train.return_value = "training_results"

    mock_yolo_class.return_value = mock_model

    trainer = Trainer()

    result = trainer._run(cfg=cfg, current_proj_dir=tmp_path)

    assert result == "training_results"
    assert trainer.latest_results == "training_results"

    mock_model.train.assert_called_once()


@patch("src.trainer.Trainer.validate_cuda")
@patch("src.trainer.YOLO")
def test_run_tune_success(
    mock_yolo_class,
    mock_validate,
    tmp_path,
):
    cfg = tmp_path / "args.yaml"

    cfg.write_text(
        yaml.dump(
            {
                "model": "yolo11n.pt",
                "imgsz": 640,
                "epochs": 50,
                "iterations": 10,
                "data": "data.yaml",
            }
        )
    )

    mock_model = MagicMock()
    mock_model.tune.return_value = "tune_results"

    mock_yolo_class.return_value = mock_model

    trainer = Trainer()

    result = trainer._run(
        cfg=cfg,
        current_proj_dir=tmp_path,
        tune=True,
    )

    assert result == "tune_results"

    mock_model.tune.assert_called_once()


@patch("src.trainer.time.sleep")
@patch("src.trainer.Trainer.validate_cuda")
@patch("src.trainer.YOLO")
def test_run_retries_after_permission_error(
    mock_yolo_class,
    mock_validate,
    mock_sleep,
    tmp_path,
):
    cfg = tmp_path / "args.yaml"

    cfg.write_text(
        yaml.dump(
            {
                "model": "yolo11n.pt",
                "imgsz": 640,
                "epochs": 50,
            }
        )
    )

    mock_model = MagicMock()

    mock_model.train.side_effect = [
        PermissionError(),
        "success"
    ]

    mock_yolo_class.return_value = mock_model

    trainer = Trainer()

    result = trainer._run(
        cfg=cfg,
        current_proj_dir=tmp_path,
    )

    assert result == "success"

    assert mock_model.train.call_count == 2
    mock_sleep.assert_called()


@patch("src.trainer.Trainer.validate_cuda")
@patch("src.trainer.YOLO")
def test_run_resume_training(
    mock_yolo_class,
    mock_validate,
    tmp_path,
):
    cfg = tmp_path / "args.yaml"

    cfg.write_text(
        yaml.dump(
            {
                "model": "yolo11n.pt",
                "imgsz": 640,
                "epochs": 50,
            }
        )
    )

    checkpoint = tmp_path / "last.pt"
    checkpoint.touch()

    resumed_model = MagicMock()
    resumed_model.train.return_value = "resumed"

    mock_yolo_class.return_value = resumed_model

    trainer = Trainer()

    result = trainer._run(
        cfg=cfg,
        current_proj_dir=tmp_path,
        resume=checkpoint,
    )

    assert result == "resumed"

    resumed_model.train.assert_called_once_with(
        resume=True
    )


# ============================================================
# count_yolo_labels
# ============================================================

def test_count_yolo_labels(tmp_path):
    labels_dir = tmp_path / "labels"
    labels_dir.mkdir()

    (labels_dir / "a.txt").write_text(
        "0 0.1 0.2\n"
        "1 0.3 0.4\n"
    )

    (labels_dir / "b.txt").write_text(
        "1 0.5 0.6\n"
        "0 0.7 0.8\n"
        "0 0.9 1.0\n"
    )

    counter = Trainer.count_yolo_labels(labels_dir)

    assert counter[0] == 3
    assert counter[1] == 2


def test_count_yolo_labels_ignores_bad_lines(tmp_path):
    labels_dir = tmp_path / "labels"
    labels_dir.mkdir()

    (labels_dir / "a.txt").write_text(
        "invalid\n"
        "0 0.5 0.6\n"
    )

    counter = Trainer.count_yolo_labels(labels_dir)

    assert counter[0] == 1


# ============================================================
# print_distribution
# ============================================================

def test_print_distribution(capsys):
    counter = Counter({0: 8, 1: 2})

    Trainer.print_distribution(
        counter,
        ["cat", "dog"],
        "TRAIN",
    )

    output = capsys.readouterr().out

    assert "TRAIN DISTRIBUTION" in output
    assert "cat" in output
    assert "dog" in output


# ============================================================
# plot_distribution
# ============================================================

def test_plot_distribution_creates_file(tmp_path):
    output = tmp_path / "plot.png"

    Trainer.plot_distribution(
        Counter({0: 5, 1: 3}),
        ["cat", "dog"],
        "Test Plot",
        output,
    )

    assert output.exists()
    assert output.stat().st_size > 0


# ============================================================
# stratified_split validation
# ============================================================

def test_stratified_split_invalid_dataset():
    trainer = Trainer()

    with pytest.raises(ValueError):
        trainer.stratified_split(
            data_dir="does_not_exist"
        )


def test_stratified_split_invalid_train_pct(tmp_path):
    trainer = Trainer()

    data_dir = tmp_path / "dataset"
    data_dir.mkdir()

    yaml_file = tmp_path / "data.yaml"
    yaml_file.write_text(
        yaml.dump({"names": ["class1"]})
    )

    with pytest.raises(ValueError):
        trainer.stratified_split(
            data_dir=data_dir,
            data_yaml=yaml_file,
            train_pct=1.0,
        )


def test_stratified_split_missing_names(tmp_path):
    trainer = Trainer()

    data_dir = tmp_path / "dataset"
    data_dir.mkdir()

    yaml_file = tmp_path / "data.yaml"
    yaml_file.write_text("{}")

    with pytest.raises(ValueError):
        trainer.stratified_split(
            data_dir=data_dir,
            data_yaml=yaml_file,
        )