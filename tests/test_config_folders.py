import os

from cbr_db.config_folders import get_absolute_path


def test_get_absolute_path():
    # For absolute path, return absolute path
    path = os.path.abspath(__file__)
    assert get_absolute_path(path) == path
