from cbr_db.filesystem import get_sqldump_table_and_filename


def test_sqldump_table_and_filename():
    assert (get_sqldump_table_and_filename('101') ==
            ('f101', 'f101.sql'))

    assert (get_sqldump_table_and_filename('102') ==
            ('f102', 'f102.sql'))
