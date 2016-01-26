import os

import pytest

from cbr_db.filesystem import get_sqldump_table_and_filename, get_public_data_folder,\
    get_csv_files


def test_sqldump_table_and_filename():
    assert (get_sqldump_table_and_filename('101') ==
            ('f101', 'f101.sql'))

    assert (get_sqldump_table_and_filename('102') ==
            ('f102', 'f102.sql'))


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
def test_get_csv_files(form, isodate, expected):
    path = get_public_data_folder(form, 'csv')
    expected = [os.path.join(path, x) for x in expected]
    assert sorted(get_csv_files(isodate, form)) == expected
