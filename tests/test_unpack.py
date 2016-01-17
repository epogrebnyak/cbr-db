import os
import shutil

import pytest

from cbr_db.unpack import get_local_ziprar_filepath, unpack_path

from .conftest import FILES_DIR, compare_dirs


def test_get_local_ziprar_filepath(mocker):
    mocker.patch('cbr_db.unpack.get_public_data_folder', return_value='dummy')
    # Older archives are in zip
    assert get_local_ziprar_filepath('2005-12-01', '101') ==\
           os.path.join('dummy', '101-20051201.zip')
    # Newer archives are in rar
    assert get_local_ziprar_filepath('2015-12-01', '101') ==\
           os.path.join('dummy', '101-20151201.rar')


@pytest.mark.parametrize('filename,form', [
    ('101-20051201.zip', '101'),
    ('101-20151201.rar', '101')
])
def test_unpack_path(mocker, tempdir, filename, form):
    test_path = os.path.join(FILES_DIR, 'unpack', os.path.splitext(filename)[0])
    input_path = os.path.join(test_path, 'input', filename)
    expected_output_dir = os.path.join(test_path, 'output')
    temp_input_path = os.path.join(tempdir, os.path.relpath(input_path, FILES_DIR))
    os.makedirs(os.path.dirname(temp_input_path))
    shutil.copy(input_path, temp_input_path)
    # Unpack into output_dir (in temp)
    output_dir = os.path.join(tempdir, os.path.relpath(expected_output_dir, FILES_DIR))
    mocker.patch('cbr_db.unpack.get_public_data_folder', return_value=output_dir)
    unpack_path(temp_input_path, form)
    compare_dirs(expected_output_dir, output_dir)
