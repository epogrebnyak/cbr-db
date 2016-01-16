from bz2 import BZ2File
import filecmp
import os
import shutil
import tempfile

import pytest


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'cbr-db-tests')
FILES_DIR = os.path.join(TESTS_DIR, 'files')


@pytest.fixture(scope='function')
def tempdir():
    """This fixture re-creates temp directory for tests."""
    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)
    return TEMP_DIR


def compare_dirs(a, b):
    _assert_equal_dirs(filecmp.dircmp(a, b))


def _assert_equal_dirs(cmp):
    assert cmp.diff_files == []
    assert cmp.funny_files == []
    assert cmp.left_only == []
    assert cmp.right_only == []
    for subcmp in cmp.subdirs:
        _assert_equal_dirs(subcmp)


def copy_and_unpack(source_dir, target_dir):
    """
    Copies files to testing location.
    Unpacks archived files.

    Returns target_dir.
    """
    shutil.copytree(source_dir, target_dir)
    for current_dir, dir_names, file_names in os.walk(target_dir):
        for file_name in file_names:
            if os.path.splitext(file_name)[1] != '.bz2':
                continue
            bz_name = os.path.join(current_dir, file_name)
            unpacked_name = os.path.join(current_dir, os.path.splitext(file_name)[0])
            with BZ2File(bz_name) as bz2file:
                with open(unpacked_name, 'wb') as file:
                    shutil.copyfileobj(bz2file, file)
            os.remove(bz_name)
    return target_dir
