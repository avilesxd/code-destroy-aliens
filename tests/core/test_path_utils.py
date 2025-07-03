import json
import os
import sys
import tempfile
from unittest import mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.core.path_utils import ensure_data_directory, get_app_directory, load_json_file, resource_path, save_json_file


def safe_setattr(obj: object, attr: str, value: object) -> None:
    if not hasattr(obj, attr):
        setattr(obj, attr, value)
    else:
        setattr(obj, attr, value)


# --- get_app_directory ---


@pytest.mark.skipif(sys.platform == "win32", reason="Avoid PosixPath error on Windows")
def test_get_app_directory_normal(monkeypatch: MonkeyPatch) -> None:
    safe_setattr(sys, "frozen", False)
    expected = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    assert get_app_directory() == expected


@pytest.mark.skipif(sys.platform == "win32", reason="Avoid PosixPath error on Windows")
def test_get_app_directory_frozen_mac_meipass(monkeypatch: MonkeyPatch) -> None:
    safe_setattr(sys, "frozen", True)
    safe_setattr(sys, "_MEIPASS", "/dummy/bundle/path")
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(sys, "executable", "/dummy/path/MacOS/App")
    assert get_app_directory() == "/dummy"


# --- ensure_data_directory ---


def test_ensure_data_directory_unix(monkeypatch: MonkeyPatch) -> None:
    if sys.platform == "win32":
        pytest.skip("Avoid PosixPath error on Windows")
    else:
        monkeypatch.setattr(os, "name", "posix")
        monkeypatch.setattr(sys, "platform", "linux")
        safe_setattr(sys, "frozen", False)
        monkeypatch.setattr("src.core.path_utils.get_app_directory", lambda: tempfile.gettempdir())
        path = ensure_data_directory()
        assert "Alien Invasion" in path
        assert os.path.exists(path)


def test_ensure_data_directory_windows(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setenv("LOCALAPPDATA", tempfile.gettempdir())
    path = ensure_data_directory()
    assert "Alien Invasion" in path
    assert os.path.exists(path)


# --- resource_path ---


def test_resource_path_dev() -> None:
    test_path = resource_path("testfile.txt")
    assert test_path.endswith("testfile.txt")


@pytest.mark.skipif(sys.platform == "win32", reason="Avoid PosixPath error on Windows")
def test_resource_path_frozen(monkeypatch: MonkeyPatch) -> None:
    safe_setattr(sys, "frozen", True)
    safe_setattr(sys, "_MEIPASS", "/dummy/path")
    test_path = resource_path("file.txt")
    assert test_path == os.path.normpath("/dummy/path/file.txt")


# --- load_json_file ---


def test_load_json_file_valid() -> None:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        json.dump({"test": 123}, tf)
        tf.seek(0)
    data = load_json_file(tf.name)
    assert data["test"] == 123
    os.unlink(tf.name)


def test_load_json_file_missing() -> None:
    data = load_json_file("nonexistent.json", default_value={"default": True})
    assert data == {"default": True}


def test_load_json_file_invalid_json() -> None:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("{ invalid json ")
    data = load_json_file(tf.name, default_value=[])
    assert data == []
    os.unlink(tf.name)


# --- save_json_file ---


def test_save_json_file_success() -> None:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        path = tf.name
    result = save_json_file(path, {"key": "value"})
    assert result is True
    with open(path, "r", encoding="utf-8") as f:
        assert json.load(f)["key"] == "value"
    os.unlink(path)


def test_save_json_file_error(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.open", mock.Mock(side_effect=PermissionError("fail")))
    result = save_json_file("/path/to/nowhere/file.json", {"x": 1})
    assert result is False
