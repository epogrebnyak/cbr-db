from contextlib import closing
from .connection import get_mysql_connection, make_insert_statement


def import_records(db, table, fields, records, record_fields):
    insert_sql = make_insert_statement(table, fields, ignore=True)
    # with autocommit turned off, the insertions should be fast
    with closing(get_mysql_connection(database=db, autocommit=False)) as conn:
        with closing(conn.cursor()) as cur:
            for record in records:
                ordered_values = [record[key] for key in record_fields]
                cur.execute(insert_sql, ordered_values)
