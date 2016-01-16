import os
import shutil
import tempfile

import pytest

TEMP_DIR = os.path.join(tempfile.gettempdir(), 'cbr-db-tests')

@pytest.fixture(scope='function')
def tempdir():
    """This fixture re-creates temp directory for tests."""
    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)
    return TEMP_DIR
