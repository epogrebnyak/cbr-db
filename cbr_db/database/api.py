from contextlib import closing
import csv
from datetime import datetime
import os

from cbr_db.conf import settings
from .connection import get_mysql_connection, make_insert_statement


def import_records(db, table, fields, records, record_fields):
    insert_sql = make_insert_statement(table, fields, ignore=True)
    # with autocommit turned off, the insertions should be fast
    with closing(get_mysql_connection(database=db, autocommit=False)) as conn:
        with closing(conn.cursor()) as cur:
            for record in records:
                ordered_values = [record[key] for key in record_fields]
                cur.execute(insert_sql, ordered_values)


def create_database():
    """
    Creates SQLite database if it doesn't exist.
    """
    if os.path.isfile(settings.DB_SQLITE):
        return
    from .models import Base, engine
    Base.metadata.create_all(engine)


def create_session():
    from .models import Session
    return Session()


def import_csv_to_database(form, csv_path, dbf_filename):
    """Import CSV into sqlite database."""
    from .models import Source
    create_database()
    if form == '101':
        import_form = _import_f101
    elif form == '102':
        import_form = _import_f102
    else:
        raise ValueError('Invalid form: {!r}'.format(form))
    with closing(create_session()) as session:
        try:
            source = Source(form=int(form), source=dbf_filename)
            session.add(source)
            session.commit()  # We need source id
            import_form(session, source, csv_path)
            session.commit()
        except:
            session.rollback()
            raise


def _import_f101(session, source, csv_path):
    """
    Bulk CSV import implementation for Form 101.
    """
    from .models import F101
    with open(csv_path) as file:
        reader = csv.DictReader(file, dialect='excel-tab')
        session.bulk_insert_mappings(F101, (
            {
                'source_id': source.id,
                'dt': datetime.strptime(x['DT'], '%Y-%m-%d'),
                'regn': x['REGN'],
                'conto': x['NUM_SC'],
                'a_p': x['A_P'],
                'itogo': x.get('ITOGO') or x['IITG'],
                'iv': x.get('IV', 0),
                'ir': x.get('IR', 0),
                'has_iv': 1 if 'IV' in x else 0,
            } for x in reader
        ))


def _import_f102(session, source, csv_path):
    """
    Bulk CSV import implementation for Form 102.
    """
    from .models import F102
    raise NotImplementedError
