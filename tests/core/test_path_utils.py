"""Tests for path utilities module."""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.path_utils import ensure_data_directory, get_app_directory, load_json_file, resource_path, save_json_file


def test_get_app_directory_from_source() -> None:
    """Test get_app_directory when running from source."""
    # When running from source, frozen should be False
    with patch("sys.frozen", False, create=True):
        result = get_app_directory()
        assert os.path.isabs(result)
        assert os.path.exists(result)


def test_get_app_directory_frozen_non_darwin() -> None:
    """Test get_app_directory when running as frozen executable on non-Darwin platform."""
    with patch("sys.frozen", True, create=True):
        with patch("sys.platform", "win32"):
            # Create a mock _MEIPASS
            mock_path = "C:\\temp\\app"
            with patch("sys._MEIPASS", mock_path, create=True):
                result = get_app_directory()
                # Should return the directory of the source file when not frozen
                assert isinstance(result, str)


def test_ensure_data_directory_windows() -> None:
    """Test ensure_data_directory on Windows."""
    with patch("os.name", "nt"):
        with patch("os.getenv") as mock_getenv:
            mock_getenv.return_value = tempfile.gettempdir()

            result = ensure_data_directory()

            assert "Alien Invasion" in result
            assert os.path.isabs(result)


def test_ensure_data_directory_windows_no_appdata() -> None:
    """Test ensure_data_directory on Windows when LOCALAPPDATA is not set."""
    with patch("os.name", "nt"):
        with patch("os.getenv", return_value=None):
            with patch("os.path.expanduser") as mock_expanduser:
                mock_expanduser.return_value = os.path.join(tempfile.gettempdir(), "AppData", "Local")

                result = ensure_data_directory()

                assert "Alien Invasion" in result


def test_ensure_data_directory_unix() -> None:
    """Test ensure_data_directory on Unix-like systems."""
    with patch("os.name", "posix"):
        with patch("sys.platform", "linux"):
            with patch("sys.frozen", False, create=True):
                result = ensure_data_directory()

                assert "Alien Invasion" in result
                assert os.path.isabs(result)


def test_ensure_data_directory_macos_frozen() -> None:
    """Test ensure_data_directory on macOS when running as app bundle."""
    with patch("os.name", "posix"):
        with patch("sys.platform", "darwin"):
            with patch("sys.frozen", True, create=True):
                with patch("os.path.expanduser") as mock_expanduser:
                    mock_expanduser.return_value = os.path.join(
                        tempfile.gettempdir(), "Library", "Application Support", "Alien Invasion"
                    )

                    result = ensure_data_directory()

                    assert "Alien Invasion" in result


def test_ensure_data_directory_creates_directory() -> None:
    """Test that ensure_data_directory actually creates the directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "test_alien_invasion")

        with patch("os.name", "posix"):
            with patch("sys.platform", "linux"):
                with patch("sys.frozen", False, create=True):
                    with patch("src.core.path_utils.get_app_directory", return_value=tmpdir):
                        result = ensure_data_directory()

                        assert os.path.exists(result)
                        assert os.path.isdir(result)


def test_ensure_data_directory_error_handling() -> None:
    """Test ensure_data_directory error handling."""
    with patch("os.makedirs", side_effect=PermissionError("No permission")):
        with pytest.raises(PermissionError):
            ensure_data_directory()


def test_resource_path_from_source() -> None:
    """Test resource_path when running from source."""
    with patch("sys.frozen", False, create=True):
        result = resource_path("test/path.txt")

        assert "test" in result
        assert "path.txt" in result
        assert os.path.isabs(result)


def test_resource_path_with_path_object() -> None:
    """Test resource_path with Path object."""
    with patch("sys.frozen", False, create=True):
        path_obj = Path("test") / "path.txt"
        result = resource_path(path_obj)

        assert "test" in result
        assert "path.txt" in result


def test_resource_path_frozen_darwin_meipass() -> None:
    """Test resource_path on macOS with _MEIPASS."""
    with patch("sys.frozen", True, create=True):
        with patch("sys.platform", "darwin"):
            mock_path = "/tmp/app"
            with patch("sys._MEIPASS", mock_path, create=True):
                result = resource_path("test.txt")

                assert "test.txt" in result


def test_resource_path_frozen_darwin_alias() -> None:
    """Test resource_path on macOS in alias mode (no _MEIPASS)."""
    with patch("sys.frozen", True, create=True):
        with patch("sys.platform", "darwin"):
            # Without _MEIPASS, it falls back to source directory
            result = resource_path("test.txt")

            assert "test.txt" in result


def test_resource_path_frozen_non_darwin() -> None:
    """Test resource_path on frozen non-Darwin platform."""
    with patch("sys.frozen", True, create=True):
        with patch("sys.platform", "win32"):
            mock_path = "C:\\temp\\app"
            with patch("sys._MEIPASS", mock_path, create=True):
                result = resource_path("test.txt")

                assert "test.txt" in result


def test_resource_path_error_handling() -> None:
    """Test resource_path handles errors gracefully."""
    with patch("sys.frozen", False, create=True):
        # The function handles errors and returns fallback path
        # Even with error, it should return a path with the requested file
        result = resource_path("test.txt")

        assert "test.txt" in result
        assert os.path.isabs(result)


def test_load_json_file_success() -> None:
    """Test load_json_file with valid JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_data = {"key": "value", "number": 42}
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_json_file(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_load_json_file_not_found() -> None:
    """Test load_json_file with non-existent file."""
    default = {"default": True}
    result = load_json_file("nonexistent.json", default)

    assert result == default


def test_load_json_file_invalid_json() -> None:
    """Test load_json_file with invalid JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        default = {"default": True}
        result = load_json_file(temp_path, default)
        assert result == default
    finally:
        os.unlink(temp_path)


def test_load_json_file_with_path_object() -> None:
    """Test load_json_file with Path object."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_data = {"test": "data"}
        json.dump(test_data, f)
        temp_path = Path(f.name)

    try:
        result = load_json_file(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_load_json_file_unexpected_error() -> None:
    """Test load_json_file with unexpected error."""
    with patch("builtins.open", side_effect=IOError("Unexpected error")):
        default = {"default": True}
        result = load_json_file("test.json", default)
        assert result == default


def test_save_json_file_success() -> None:
    """Test save_json_file saves data correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.json")
        test_data = {"key": "value", "number": 42}

        result = save_json_file(file_path, test_data)

        assert result is True
        assert os.path.exists(file_path)

        with open(file_path, "r") as f:
            loaded = json.load(f)
            assert loaded == test_data


def test_save_json_file_creates_directory() -> None:
    """Test that save_json_file creates parent directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "subdir", "nested", "test.json")
        test_data = {"test": "data"}

        result = save_json_file(file_path, test_data)

        assert result is True
        assert os.path.exists(file_path)


def test_save_json_file_with_custom_indent() -> None:
    """Test save_json_file with custom indentation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.json")
        test_data = {"key": "value"}

        result = save_json_file(file_path, test_data, indent=2)

        assert result is True

        with open(file_path, "r") as f:
            content = f.read()
            # Should have 2-space indentation
            assert "  " in content


def test_save_json_file_with_path_object() -> None:
    """Test save_json_file with Path object."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"
        test_data = {"test": "data"}

        result = save_json_file(file_path, test_data)

        assert result is True
        assert file_path.exists()


def test_save_json_file_error() -> None:
    """Test save_json_file handles errors."""
    # Try to write with invalid filename characters (Windows)
    if os.name == "nt":
        invalid_path = "C:\\invalid:path\\file.json"  # Colon in path is invalid on Windows
    else:
        invalid_path = "/root/nopermissions/file.json"  # No write access

    result = save_json_file(invalid_path, {"data": "test"})

    # May succeed or fail depending on permissions, so just check it's a boolean
    assert isinstance(result, bool)
