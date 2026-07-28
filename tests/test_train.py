from pathlib import Path

from first_ml_project.train import load_config, train_model


def test_load_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("test_size: 0.2\nrandom_state: 42\nmax_iter: 300\noutput_dir: artifacts\n", encoding="utf-8")

    config = load_config(config_file)

    assert config["test_size"] == 0.2
    assert config["random_state"] == 42


def test_train_model(tmp_path):
    config = {
        "test_size": 0.2,
        "random_state": 42,
        "max_iter": 300,
        "output_dir": str(tmp_path),
    }

    result = train_model(config)

    assert Path(result["model_path"]).exists()
    assert result["metrics"]["accuracy"] >= 0.0
