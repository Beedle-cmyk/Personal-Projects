from pathlib import Path
import yaml
import pytest

from src.project_manager import ProjectManager


@pytest.fixture
def mock_cfg_directory(tmp_path, monkeypatch):
    """
    Creates fake args.yaml and tune_args.yaml files and patches
    CFG_DIRECTORY so tests do not depend on real project files.
    """

    cfg_source = tmp_path / "cfg_source"
    cfg_source.mkdir()

    (cfg_source / "args.yaml").write_text(
        """
data: data.yaml
epochs: 100
"""
    )

    (cfg_source / "tune_args.yaml").write_text(
        """
data: data.yaml
iterations: 50
"""
    )

    monkeypatch.setattr(
        "src.project_manager.CFG_DIRECTORY",
        cfg_source
    )

    return cfg_source


class TestCountData:

    def test_counts_supported_images(self, tmp_path):
        (tmp_path / "a.jpg").write_text("")
        (tmp_path / "b.jpeg").write_text("")
        (tmp_path / "c.png").write_text("")
        (tmp_path / "ignore.txt").write_text("")

        pm = ProjectManager(tmp_path)

        count = pm.count_data(tmp_path)

        assert count == 3
        assert pm.data_num == 3

    def test_counts_nested_images(self, tmp_path):
        subdir = tmp_path / "nested"
        subdir.mkdir()

        (subdir / "a.jpg").write_text("")
        (subdir / "b.png").write_text("")

        pm = ProjectManager(tmp_path)

        assert pm.count_data(tmp_path) == 2

    def test_raises_for_invalid_directory(self):
        pm = ProjectManager(".")

        with pytest.raises(ValueError):
            pm.count_data("does_not_exist")


class TestUpdateFindings:

    def test_writes_file(self, tmp_path):
        pm = ProjectManager(tmp_path)

        findings_file = tmp_path / "findings.txt"

        pm.update_findings(findings_file, "test contents")

        assert findings_file.read_text() == "test contents"


class TestGetLabelsFromConfig:

    def test_extracts_labels(self, tmp_path):
        xml_file = tmp_path / "config.xml"

        xml_file.write_text(
            """
<View>
    <Labels name="label">
        <Label value="Dog"/>
        <Label value="Cat"/>
        <Label value="Bird"/>
    </Labels>
</View>
"""
        )

        labels = ProjectManager.get_labels_from_config(xml_file)

        assert labels == ["Dog", "Cat", "Bird"]

    def test_returns_empty_list_when_no_labels(self, tmp_path):
        xml_file = tmp_path / "config.xml"

        xml_file.write_text("<View></View>")

        labels = ProjectManager.get_labels_from_config(xml_file)

        assert labels == []


class TestUpdateCfgs:

    def test_updates_data_path(self, tmp_path):
        cfg_dir = tmp_path / "cfg"
        cfg_dir.mkdir()

        working_dir = tmp_path / "project"

        source_yaml = tmp_path / "args.yaml"

        source_yaml.write_text(
            """
data: data.yaml
epochs: 100
"""
        )

        ProjectManager._update_cfgs(
            cfg_dir=cfg_dir,
            yaml_path=source_yaml,
            working_dir=working_dir,
        )

        updated_yaml = cfg_dir / "args.yaml"

        data = yaml.safe_load(updated_yaml.read_text())

        assert data["data"] == str(working_dir / "data.yaml")
        assert data["epochs"] == 100


class TestCreateProject:

    def test_creates_project_structure(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        pm = ProjectManager(tmp_path)

        project = pm.create_project(
            name="test_project"
        )

        assert project.exists()

        assert (project / "cfg").exists()
        assert (project / "runs").exists()
        assert (project / "prelabels").exists()
        assert (project / "labelstudio").exists()

        assert (project / "original_data").exists()
        assert (project / "original_data" / "images").exists()
        assert (project / "original_data" / "labels").exists()

        assert (project / "findings.txt").exists()
        assert (project / "data.yaml").exists()

    def test_sets_current_project(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        pm = ProjectManager(tmp_path)

        project = pm.create_project(name="project")

        assert pm.current_proj == project

    def test_duplicate_project_raises(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        pm = ProjectManager(tmp_path)

        pm.create_project(name="project")

        with pytest.raises(FileExistsError):
            pm.create_project(name="project")

    def test_invalid_project_type_raises(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        pm = ProjectManager(tmp_path)

        with pytest.raises(ValueError):
            pm.create_project(
                name="project",
                project_type="classification"
            )

    def test_copies_image_data(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        data_source = tmp_path / "dataset"
        data_source.mkdir()

        (data_source / "image1.jpg").write_text("")
        (data_source / "image2.png").write_text("")

        pm = ProjectManager(tmp_path)

        project = pm.create_project(
            name="project",
            data_dir=data_source,
        )

        images_dir = project / "original_data" / "images"

        assert (images_dir / "image1.jpg").exists()
        assert (images_dir / "image2.png").exists()

    def test_updates_yaml_using_label_config(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        xml_file = tmp_path / "labels.xml"

        xml_file.write_text(
            """
<View>
    <Labels>
        <Label value="Staining"/>
        <Label value="Crack"/>
        <Label value="Void"/>
    </Labels>
</View>
"""
        )

        pm = ProjectManager(tmp_path)

        project = pm.create_project(
            name="project",
            label_config=xml_file,
        )

        data_yaml = yaml.safe_load(
            (project / "data.yaml").read_text()
        )

        assert data_yaml["names"] == [
            "Staining",
            "Crack",
            "Void",
        ]

        assert data_yaml["nc"] == 3


class TestUpdateYamlPaths:

    def test_updates_all_yaml_paths(
        self,
        tmp_path,
        mock_cfg_directory,
    ):
        pm = ProjectManager(tmp_path)

        project = pm.create_project(
            name="project"
        )

        pm.update_yaml_paths(project)

        data_yaml = yaml.safe_load(
            (project / "data.yaml").read_text()
        )

        args_yaml = yaml.safe_load(
            (project / "cfg" / "args.yaml").read_text()
        )

        tune_yaml = yaml.safe_load(
            (project / "cfg" / "tune_args.yaml").read_text()
        )

        assert data_yaml["path"] == str(project / "data")
        assert args_yaml["data"] == str(project / "data.yaml")
        assert tune_yaml["data"] == str(project / "data.yaml")