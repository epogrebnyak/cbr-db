"""
Test script for SQLite database.
Checks that data in MySQL and SQLite databases are the same.

NOTE: This script does not collect data, it just checks it.
To collect data, run wrapper.py with appropriate arguments.
"""

import argparse
from contextlib import closing
import csv
import os
import shutil
import sqlite3
import sys
import tempfile

PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, PROJECT_PATH)

from cbr_db.conf import settings
from cbr_db.database.connection import get_mysql_connection


TEMPDIR = os.path.join(tempfile.gettempdir(), 'cbr-db-compare')


def export_to_csv(cursor, table, columns, order, file_path):
    query = 'SELECT {} FROM {} ORDER BY {}'.format(', '.join(columns), table, ', '.join(order))
    cursor.execute(query)
    count = 0
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        while True:
            row = cursor.fetchone()
            if not row:
                break
            writer.writerow(row)
            count += 1
    print('Exported {} rows to {}'.format(count, file_path))


def check_f101(sqlite, mysql):
    sqlite.execute('SELECT count(*) FROM f101')
    mysql.execute('SELECT count(*) FROM f101')
    sqlite_count = sqlite.fetchone()[0]
    mysql_count = mysql.fetchone()[0]
    if sqlite_count != mysql_count:
        print('SQLite {} rows, MySQL {} rows'.format(sqlite_count, mysql_count))
    columns = ['dt', 'regn', 'conto', 'a_p', 'ir', 'iv', 'itogo', 'has_iv']
    order = ['dt', 'regn', 'conto']
    export_to_csv(sqlite, 'f101', columns, order, os.path.join(TEMPDIR, 'f101_sqlite.csv'))
    export_to_csv(mysql, 'f101', columns, order, os.path.join(TEMPDIR, 'f101_mysql.csv'))


def check_f102(sqlite, mysql):
    sqlite.execute('SELECT * FROM f101')
    mysql.execute()
    pass


_FUNCTIONS = {
    '101': check_f101,
    '102': check_f102,
}


def _parse_args(argv):
    parser = argparse.ArgumentParser(description='Check that MySQL and SQLite results match')
    parser.add_argument('form')
    return parser.parse_args(argv)


def main(argv):
    args = _parse_args(argv)
    if os.path.isdir(TEMPDIR):
        shutil.rmtree(TEMPDIR)
    os.mkdir(TEMPDIR)
    check = _FUNCTIONS[args.form]
    with closing(sqlite3.connect(settings.DB_SQLITE)) as sqlite_conn,\
            closing(get_mysql_connection('dbf_db')) as mysql_conn:
        sqlite = sqlite_conn.cursor()
        mysql = mysql_conn.cursor()
        check(sqlite, mysql)


if __name__ == '__main__':
    if 'CBR_DB_SETTINGS' not in os.environ:
        os.environ['CBR_DB_SETTINGS'] = 'settings'
    main(sys.argv[1:])
