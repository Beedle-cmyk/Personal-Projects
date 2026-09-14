from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

from src.auto_trainer import AutoTrainer


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def auto_trainer():
    with (
        patch("src.auto_trainer.ProjectManager") as mock_pm,
        patch("src.auto_trainer.Trainer") as mock_trainer,
    ):
        pm = mock_pm.return_value
        pm.current_proj = Path("project_10")

        trainer = AutoTrainer(
            proj_dir="projects",
            data_dir="data",
        )

        yield trainer


# ------------------------------------------------------------------
# __init__
# ------------------------------------------------------------------

def test_init_creates_dependencies():
    with (
        patch("src.auto_trainer.ProjectManager") as mock_pm,
        patch("src.auto_trainer.Trainer") as mock_trainer,
    ):
        trainer = AutoTrainer(
            proj_dir="projects",
            data_dir="data",
        )

        mock_pm.assert_called_once_with("projects")
        mock_trainer.assert_called_once()

        assert trainer.data_dir == "data"
        assert trainer.current_proj_dir is None
        assert trainer.model is None
        assert trainer._studio_running is False


# ------------------------------------------------------------------
# setup_project
# ------------------------------------------------------------------

def test_setup_project_without_labels(auto_trainer):
    auto_trainer.setup_project()

    auto_trainer.project_manager.create_project.assert_called_once_with(
        data_dir="data",
        label_config=None,
    )

    assert auto_trainer.current_proj_dir == Path("project_10")


@patch("src.auto_trainer.shutil.copy")
@patch("src.auto_trainer.LabelStudioManager.seg_json_to_yolo")
def test_setup_project_with_labels(
    mock_seg,
    mock_copy,
    auto_trainer,
):
    auto_trainer.project_manager.count_data.return_value = 3

    mock_file_1 = Mock()
    mock_file_1.is_file.return_value = True

    mock_file_2 = Mock()
    mock_file_2.is_file.return_value = True

    with patch.object(auto_trainer, "cleanup_images") as mock_cleanup:
        with patch.object(
            Path,
            "iterdir",
            return_value=[mock_file_1, mock_file_2],
        ):
            auto_trainer.setup_project(
                label_json="labels.json",
            )

            mock_copy.assert_called_once()
            mock_seg.assert_called_once()
            mock_cleanup.assert_called_once()


def test_setup_project_raises_when_more_labels_than_images(auto_trainer):
    auto_trainer.project_manager.count_data.return_value = 1

    mock_file_1 = Mock()
    mock_file_1.is_file.return_value = True

    mock_file_2 = Mock()
    mock_file_2.is_file.return_value = True

    with (
        patch("src.auto_trainer.shutil.copy"),
        patch("src.auto_trainer.LabelStudioManager.seg_json_to_yolo"),
        patch.object(
            Path,
            "iterdir",
            return_value=[mock_file_1, mock_file_2],
        ),
    ):
        with pytest.raises(
            ValueError,
            match="More Labels than Image files",
        ):
            auto_trainer.setup_project(label_json="labels.json")


# ------------------------------------------------------------------
# run
# ------------------------------------------------------------------

def test_run_train(auto_trainer):
    auto_trainer.current_proj_dir = "project"

    auto_trainer.trainer.train.return_value = "model"

    auto_trainer.run()

    auto_trainer.trainer.train.assert_called_once()
    assert auto_trainer.model == "model"


def test_run_tune(auto_trainer):
    auto_trainer.current_proj_dir = "project"

    auto_trainer.trainer.tune.return_value = "tuned_model"

    auto_trainer.run(tune=True)

    auto_trainer.trainer.tune.assert_called_once()
    assert auto_trainer.model == "tuned_model"


def test_run_with_explicit_project(auto_trainer):
    auto_trainer.trainer.train.return_value = "model"

    auto_trainer.run(current_proj_dir="project")

    assert auto_trainer.current_proj_dir == "project"
    auto_trainer.trainer.train.assert_called_once()


def test_run_without_project_raises(auto_trainer):
    with pytest.raises(
        ValueError,
        match="No Valid Project Directory provided",
    ):
        auto_trainer.run()


# ------------------------------------------------------------------
# default_prelabel
# ------------------------------------------------------------------

@patch("src.auto_trainer.Prelabeler")
def test_default_prelabel(mock_prelabeler, auto_trainer):
    prelabel_instance = mock_prelabeler.return_value

    auto_trainer.default_prelabel(
        model_path="model.pt",
        min_conf=0.25,
        max_conf=0.75,
        image_dir="images",
    )

    mock_prelabeler.assert_called_once_with(
        model_path="model.pt",
        min_conf=0.25,
        max_conf=0.75,
        image_dir="images",
        output_dir=Path.cwd(),
    )

    prelabel_instance.seg_predict.assert_called_once()


@patch("src.auto_trainer.Prelabeler")
def test_default_prelabel_project_prelabels(
    mock_prelabeler,
    auto_trainer,
):
    prelabel_instance = mock_prelabeler.return_value

    auto_trainer.current_proj_dir = Path("project")

    auto_trainer.default_prelabel(
        model_path="model.pt",
        min_conf=0.25,
        max_conf=0.75,
        image_dir="images",
    )

    assert (
        prelabel_instance.output_dir
        == Path("project") / "prelabels"
    )

    prelabel_instance.seg_predict.assert_called_once()


# ------------------------------------------------------------------
# studio_launch
# ------------------------------------------------------------------

@patch("src.auto_trainer.LabelStudioManager")
def test_studio_launch(mock_ls, auto_trainer):
    auto_trainer.studio_launch(
        api_key="apikey",
        ls_path="labelstudio",
    )

    mock_ls.assert_called_once_with(
        api_key="apikey",
        data_dir="data",
        ls_path="labelstudio",
        launch=False,
    )

    assert auto_trainer._studio_running is True


# ------------------------------------------------------------------
# update_best_hyperparameters
# ------------------------------------------------------------------

def test_update_best_hyperparameters(auto_trainer, tmp_path):
    project_dir = tmp_path / "project"
    cfg_dir = project_dir / "cfg"

    cfg_dir.mkdir(parents=True)

    args_yaml = cfg_dir / "args.yaml"
    best_yaml = project_dir / "best_hyperparameters.yaml"

    with open(args_yaml, "w") as f:
        yaml.safe_dump(
            {
                "lr0": 0.01,
                "momentum": 0.9,
                "epochs": 100,
            },
            f,
        )

    with open(best_yaml, "w") as f:
        yaml.safe_dump(
            {
                "lr0": 0.02,
                "momentum": 0.95,
                "epochs": 500,
            },
            f,
        )

    auto_trainer.update_best_hyperparameters(
        current_proj_dir=project_dir,
        yaml_path=best_yaml,
    )

    with open(args_yaml, "r") as f:
        updated = yaml.safe_load(f)

    assert updated["lr0"] == 0.02
    assert updated["momentum"] == 0.95

    # excluded values should not be modified
    assert updated["epochs"] == 100


def test_update_best_hyperparameters_no_yaml_found(
    auto_trainer,
    tmp_path,
):
    with pytest.raises(
        FileNotFoundError,
        match="No best_hyperparameters.yaml found",
    ):
        auto_trainer.update_best_hyperparameters(
            current_proj_dir=tmp_path,
        )