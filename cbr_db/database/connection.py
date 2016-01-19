import contextlib
from contextlib import closing

import pymysql

from ..conf import settings


def get_credentials():
    return {
        'host': settings.MYSQL_HOST,
        'port': settings.MYSQL_PORT,
        'user': settings.MYSQL_USER,
        'passwd': settings.MYSQL_PASSWORD,
        # TODO: there is no actual reason not to use UTF-8 in a database
        'charset': 'cp866'
    }


def get_mysql_connection(database, autocommit=False):
    credentials = get_credentials()
    if database is not None:
        credentials['db'] = database
    credentials['autocommit'] = autocommit
    return pymysql.connect(**credentials)


def execute_sql_with_cursor(sql_string, cur, verbose=False):
    """
    Executes a SQL query with an existing cursor, returning all the
    results (if any).
    """
    cur.execute(sql_string)
    if verbose is True:
        print(cur.description)
    return cur.fetchall()


def execute_sql(sql_string, database=None, verbose=False):
    """
    Executes a SQL query, returning all the results. A new connection is
    opened and closed at every call by using the default credentials.
    """
    with closing(get_mysql_connection(database)) as conn:
        with closing(conn.cursor()) as cur:
            result = execute_sql_with_cursor(sql_string, cur, verbose)
            conn.commit()
    return result


def clear_table(db, table):
    """
    Removes all entries from <table> at <db>.
    """
    with closing(get_mysql_connection(db)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM `{}`".format(table))
            conn.commit()


def make_insert_statement(table, fields, ignore=False):
    """
    Creates an insert SQL statement that insert a row into <table> using
    columns <fields>. The statement is built using placeholders (%s) to use
    to ensure proper value quoting.
    If <ignore> is True, then rows with repeated primary keys will be
    ignored.
    """
    mode = "IGNORE" if ignore else ""

    insert_sql = "INSERT {} INTO {} ({}) VALUES ({})".format(
        mode,
        table,
        ",".join(fields),
        ",".join(["%s"]*len(fields))
    )

    return insert_sql


def insert_rows_into_table(db, table, fields, values, ignore=False):
    """
    Inserts <values> into <db> <table> <fields>. Should only be used when
    <values> are  small enought for all values to fit in memory. If ignore is
    True, duplicates will be ignored.
    """
    sql = make_insert_statement(table, fields, ignore)
    with closing(get_mysql_connection(database=db)) as conn:
        with closing(conn.cursor()) as cur:
            for row in values:
                cur.execute(sql, row)
            conn.commit()
