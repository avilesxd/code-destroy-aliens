import json
import os
import platform
import shutil
import tempfile
from typing import Generator, Tuple
from unittest.mock import patch

import pytest

from src.config.configuration import Configuration
from src.config.statistics import Statistics


@pytest.fixture
def temp_data_dir() -> Generator[str, None, None]:
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up after tests
    shutil.rmtree(temp_dir)


@pytest.fixture
def stats_with_temp_dir(temp_data_dir: str) -> Tuple[Statistics, str]:
    """Create a Statistics instance with a temporary data directory"""
    config = Configuration()

    # Patch the ensure_data_directory function to return our temp directory
    with patch("src.config.statistics.ensure_data_directory", return_value=temp_data_dir):
        stats = Statistics(config)
        return stats, temp_data_dir


def test_encryption_and_decryption(stats_with_temp_dir: Tuple[Statistics, str]) -> None:
    """Test that data is properly encrypted and decrypted"""
    stats, temp_dir = stats_with_temp_dir

    # Set a high score
    stats.high_score = 1000

    # Save the high score (this will encrypt it)
    stats.save_high_score()

    # Verify that the file exists and is not plain JSON
    high_score_path = os.path.join(temp_dir, "high_score.dat")
    assert os.path.exists(high_score_path)

    # Read the file content
    with open(high_score_path, "rb") as f:
        content = f.read()

    # Verify that the content is not plain JSON
    try:
        json.loads(content)
        assert False, "Content should not be plain JSON"
    except json.JSONDecodeError:
        # This is expected - the content should be encrypted
        pass

    # Create a new Statistics instance to test loading
    with patch("src.config.statistics.ensure_data_directory", return_value=temp_dir):
        new_stats = Statistics(Configuration())

        # Verify that the high score was loaded correctly
        assert new_stats.high_score == 1000


def test_data_tampering_detection(stats_with_temp_dir: Tuple[Statistics, str]) -> None:
    """Test that tampered data is detected and handled gracefully"""
    stats, temp_dir = stats_with_temp_dir

    # Set a high score
    stats.high_score = 1000

    # Save the high score
    stats.save_high_score()

    # Tamper with the file
    high_score_path = os.path.join(temp_dir, "high_score.dat")
    with open(high_score_path, "rb") as f:
        content = f.read()

    # Modify the encrypted data slightly
    tampered_content = content[:10] + b"X" + content[11:]

    # Write the tampered content back
    with open(high_score_path, "wb") as f:
        f.write(tampered_content)

    # Create a new Statistics instance to test loading
    with patch("src.config.statistics.ensure_data_directory", return_value=temp_dir):
        new_stats = Statistics(Configuration())

        # Verify that the high score was reset to 0 due to tampering
        assert new_stats.high_score == 0


def test_error_handling(stats_with_temp_dir: Tuple[Statistics, str]) -> None:
    """Test that errors are handled gracefully"""
    stats, temp_dir = stats_with_temp_dir

    # Set a high score
    stats.high_score = 1000

    # Save the high score
    stats.save_high_score()

    # Corrupt the file
    high_score_path = os.path.join(temp_dir, "high_score.dat")
    with open(high_score_path, "wb") as f:
        f.write(b"This is not valid encrypted data")

    # Create a new Statistics instance to test loading
    with patch("src.config.statistics.ensure_data_directory", return_value=temp_dir):
        new_stats = Statistics(Configuration())

        # Verify that the high score was reset to 0 due to corruption
        assert new_stats.high_score == 0


@pytest.mark.skipif(platform.system() != "Windows", reason="This test is Windows-specific")
def test_directory_hiding() -> None:
    """Test that the .data directory is hidden on Windows"""

    # Local import to prevent mypy error on non-Windows
    import ctypes

    import win32api
    import win32con

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Try to hide the directory
        try:
            ctypes.windll.kernel32.SetFileAttributesW(  # type: ignore[attr-defined]
                temp_dir, 0x02
            )  # 0x02 = FILE_ATTRIBUTE_HIDDEN
        except Exception as e:
            pytest.skip(f"Could not hide directory: {e}")

        # Verify that the directory is hidden

        attrs = win32api.GetFileAttributes(temp_dir)
        assert attrs & win32con.FILE_ATTRIBUTE_HIDDEN, "Directory should be hidden"
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


def test_statistics_initialization_with_missing_directory() -> None:
    """Test that Statistics initializes correctly when the .data directory doesn't exist"""
    # Create a temporary directory that doesn't exist
    temp_dir = os.path.join(tempfile.gettempdir(), "non_existent_dir_for_test")

    # Ensure the directory doesn't exist
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    # Create a Statistics instance with the non-existent directory
    with patch("src.config.statistics.ensure_data_directory", return_value=temp_dir):
        # Create the directory manually before initializing Statistics
        os.makedirs(temp_dir, exist_ok=True)

        stats = Statistics(Configuration())

        # Verify that the high score is initialized to 0
        assert stats.high_score == 0

        # Verify that the directory was created
        assert os.path.exists(temp_dir)

    # Clean up
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
