import os

import pytest

from cbr_db.commands import dbf2csv

from .conftest import FILES_DIR, compare_dirs, copy_and_unpack


@pytest.mark.parametrize('form', ['101'])
def test_dbf2csv(mocker, tempdir, form):
    tempdir = os.path.join(tempdir, 'dbf2csv', form)
    form_dir = os.path.join(FILES_DIR, 'dbf2csv', form)
    dbf_dir = copy_and_unpack(
        os.path.join(form_dir, 'dbf'),
        os.path.join(tempdir, 'dbf')
    )
    expected_csv_dir = copy_and_unpack(
        os.path.join(form_dir, 'csv'),
        os.path.join(tempdir, 'expected-csv')
    )
    output_csv_dir = os.path.join(tempdir, 'csv')
    if not os.path.isdir(output_csv_dir):
        os.makedirs(output_csv_dir)

    def get_public_data_folder_mock(form, ext):
        assert form == '101'
        if ext == 'dbf':
            return dbf_dir
        elif ext == 'csv':
            return output_csv_dir
        assert False, 'Unexpected ext: {!r}'.format(ext)

    mocker.patch('cbr_db.commands.get_public_data_folder',
                 get_public_data_folder_mock)
    dbf2csv('2015-12-20', '101')
    compare_dirs(output_csv_dir, expected_csv_dir)
