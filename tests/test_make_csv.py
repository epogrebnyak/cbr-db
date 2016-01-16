import os

import pytest

from cbr_db.config_folders import get_public_data_folder
from cbr_db.make_csv import dbf2csv, list_csv_filepaths_by_date

from .conftest import FILES_DIR, compare_dirs, copy_and_unpack


@pytest.mark.parametrize('form', ['101'])
def test_dbf2csv(mocker, tempdir, form):
    tempdir = os.path.join(tempdir, 'dbf2csv', form)
    form_dir = os.path.join(FILES_DIR, 'dbf2csv', form)
    dbf_dir = copy_and_unpack(
        os.path.join(form_dir, 'dbf'),
        os.path.join(tempdir, 'dbf')
    )
    csv_dir = copy_and_unpack(
        os.path.join(form_dir, 'csv'),
        os.path.join(tempdir, 'expected-csv')
    )
    output_dir = os.path.join(tempdir, 'csv')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    mocker.patch('cbr_db.make_csv.get_public_data_folder',
                 lambda form, ext: dbf_dir if ext == 'dbf' else output_dir)
    dbf2csv('2015-12-20', '101')
    compare_dirs(output_dir, csv_dir)


@pytest.mark.parametrize('form,isodate,expected', [
    ('101', '2015-12-01', [
        'bulk_f101_b.112015_B',
        'bulk_f101b1.112015B1',
    ]),
    ('102', '2016-01-01', [
        'bulk_f102_P.42015_P',
        'bulk_f102_P1.42015_P1',
    ]),
])
def test_csv_filepaths_by_date(form, isodate, expected):
    path = get_public_data_folder(form, 'csv')
    expected = [os.path.join(path, x) for x in expected]
    assert sorted(list_csv_filepaths_by_date(isodate, form)) == expected
