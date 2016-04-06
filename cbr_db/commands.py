import os

from cbr_db.utils.text import read_regn_file
from .csvtools import write_csv_by_path
from .conf import settings
from .database.api import import_records, import_csv_to_database
from .database.connection import execute_sql, clear_table, insert_rows_into_table
from .database.process import mysqlimport_generic, source_sql_file, dump_table_csv,\
    run_sql_string, mysqlimport, dump_table_sql, patch_sql_file, mysqldump
from .dbftools.formats import get_import_dbf_path_for_bank, get_import_dbf_path_for_plan
from .dbftools.reader import get_records
from .filesystem import get_database_folder, prepare_output_dir,\
    get_sqldump_table_and_filename, get_private_data_folder, get_db_dumpfile_path,\
    get_csv_files, make_dbf_filename, make_csv_filename, get_public_data_folder
from .global_ini import get_account_name_parameters, BANK_TABLE_NAME, BANK_TABLE_FIELDS,\
    BANK_DBF_FIELDS, FORM_DATA
from .make_xlsx import make_xlsx
from .utils.dates import get_date, iso2date


__all__ = [
    'create_final_dataset_in_raw_database',
    'dbf2csv',
    'delete_and_create_db',
    'import_alloc',
    'import_bank',
    'import_csv',
    'import_csv_derived_from_text_files',
    'import_csv_sqlite',
    'import_dataset_from_sql',
    'import_plan',
    'import_tables',
    'load_db_from_dump',
    'make_balance',
    'report_balance_tables_csv',
    'report_balance_tables_xls',
    'save_dataset_as_sql',
    'save_db_to_dump',
    'test_balance'
]


def load_db_from_dump(db_name):
    """
    Loads a database structure from a dump file.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    """
    print("Database:", db_name)
    path = get_db_dumpfile_path(db_name)
    source_sql_file(patch_sql_file(path), db_name)
    print("Loaded database structure from file <{0}.sql>. No data was imported.".format(
        db_name))


def import_alloc(filename='alloc_raw.txt'):
    """
    TODO: describe what this function does
    """
    database = settings.DB_NAME_FINAL
    path = os.path.join(get_database_folder('alloc'), filename)
    mysqlimport_generic(database, path)


def import_bank():
    """
    Imports bank names into the final database, removing all
    previous entries.
    """
    form = '101'
    db = settings.DB_NAME_FINAL
    dbf_names = get_import_dbf_path_for_bank(form)
    clear_table(db, BANK_TABLE_NAME)
    for dbf_name, fields, dbf_fields in zip(dbf_names, BANK_TABLE_FIELDS, BANK_DBF_FIELDS):
        print("Importing bank names from {}".format(dbf_name))
        import_dbf_generic(dbf_name, db, BANK_TABLE_NAME, fields, dbf_fields)
        print("-> Done")
    execute_sql(u"INSERT IGNORE INTO bank (regn, regn_name) VALUE (964, 'Внешэкономбанк')", db)


def import_plan(form):
    """
    Imports account names of <form> into the final database, removing all
    previous entries.
    """
    db = settings.DB_NAME_FINAL

    dbf = get_import_dbf_path_for_plan(form)
    table, fields, dbf_fields = get_account_name_parameters(form)

    print("Importing account names from {}...".format(dbf))

    clear_table(db, table)
    import_dbf_generic(dbf, db, table, fields, dbf_fields)

    print("-> Done.")


def import_dbf_generic(dbf_path, db, table, fields, dbf_fields=None):
    """
    Imports a dbf file to a database directly, without using temporary files.
    The dbf file is located at <dbf_path>, and the data is imported to
    <db>.<table>, using fields <fields>. Repeated rows (same primary key) are
    ignored by default.
    """
    fields = list(fields)  # to accept generators
    # table fields can be different from the dbf fields
    if dbf_fields is None:
        dbf_fields = fields
    records = get_records(dbf_path, dbf_fields)
    import_records(db, table, fields, records, dbf_fields)


def import_tables():
    """
    TODO: describe what this function does
    """
    database = settings.DB_NAME_FINAL
    directory = get_database_folder('tables')

    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if file.endswith(".txt"):
            mysqlimport_generic(database, path)
        if file.endswith(".sql"):
            source_sql_file(path, database)
            # Risk: import_generic and source_sql_file - similar functions
            # different arg order


def save_db_to_dump(db_name):
    """
    Saves the structure of a database to a sql dump file in the standard location.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    # Other variety: http://code.activestate.com/recipes/286223-ohmysqldump/
    """
    mysqldump(db_name)


def test_balance():
    """
    TODO: describe what this function does
    """
    def do_output(sql):
        print('-> ' + sql)
        out = execute_sql(sql, settings.DB_NAME_FINAL, verbose=False)
        # Risk: I see no valuable info with verbose=True, as I'm printing the results here
        if out:
            for row, val in enumerate(out, 1):
                print("row {0}: {1}".format(row, val))
        else:
            print('No output')

        print()

    do_output('select "Test: balance residuals" as Test')
    do_output('select * from test_balance_residual')
    do_output('select "Test: ref items" as Test')
    do_output('select * from test_ref_items')
    do_output('select "Test: net assets not zero" as Test')
    do_output(
        'select dt, regn, itogo from balance where line = 500 and itogo != 0 order by dt')


def make_balance():
    """
    TODO: describe what this function does
    """
    db_name = settings.DB_NAME_FINAL
    execute_sql("call alloc_make", db_name)
    execute_sql("delete from balance", db_name)
    execute_sql("call balance_make", db_name)
    # use cbr_db2;
    # call alloc_make;
    # delete from balance;
    # call balance_make;


def report_balance_tables_xls():
    """
    TODO: describe what this function does
    """
    report_balance_tables_csv()
    prepare_output_dir(settings.OUTPUT_DIR)
    make_xlsx(settings.OUTPUT_DIR)


def report_balance_tables_csv():
    """
    TODO: describe what this function does and change wording
    """
    # prepare TABLES in database
    db_name = settings.DB_NAME_FINAL
    execute_sql("call balance_report_line_dt_3tables", db_name)

    # dump TABLES to CSV
    prepare_output_dir(settings.OUTPUT_DIR)
    TABLES = ("tmp_output_itogo", "tmp_output_ir", "tmp_output_iv")
    for table in TABLES:
        dump_table_csv(db_name, table, settings.OUTPUT_DIR)


def create_final_dataset_in_raw_database(form, timestamp1, timestamp2=None,
                                         regn_list=None, regn_file=None,
                                         regn_all=True):
    """
    Processes the data from the raw database, creating the final dataset for
    <form>.
    <timestamp1> and <timestamp2> can be set to limit the dates that goes
    to the final dataset.

    <regn_list> can be set to a string containing the registration numbers,
    separated by comma, that will be selected to the final database.

    <regn_file> (optional) can be the path to a file containing the registration
    numbers, one in each line of the file.

    If <regn_all> is True, all possible registration numbers can be selected to
    go to the final database.

    Only one regn selection mechanism should be set at the same time. Priority is
    given in this order: <regn_list>, <regn_file>, and <regn_all>. If no regn
    mechanism was selected, <regn_all> is used.
    """
    db = settings.DB_NAME_RAW

    # date handling
    clear_table(db, "cfg_date_limit")

    def to_date(x):
        try:
            return get_date(x)[0]
        except Exception:  # TODO: catch specific exception here
            return None

    insert_rows_into_table(
        db=db,
        table="cfg_date_limit",
        fields=('dt_start', 'dt_end'),
        values=[(to_date(timestamp1), to_date(timestamp2))]
    )

    run_sql_string("call cfg_init_populate_dates();", db)

    # regn handling
    clear_table(db, "cfg_regn_in_focus")

    if not regn_list and not regn_file:
        regn_all = True

    if not regn_all:
        # get regn list and insert it to the database
        if regn_list:
            regn = regn_list.split(',')
        elif regn_file:
            regn = read_regn_file(regn_file)

        insert_rows_into_table(
            db=db,
            table="cfg_regn_in_focus",
            fields=('regn', ),
            values=regn
        )
    else:
        # populate all regn from a stored procedure
        run_sql_string("call cfg_init_regn_fullset();", db)

    # make the final dataset in the raw database
    run_sql_string("call f{}_make_dataset();".format(form), db)


def import_dataset_from_sql(form):
    """
    Imports a dataset from the default sql dump file.
    """
    prepare_output_dir(settings.OUTPUT_DIR)
    filename = get_sqldump_table_and_filename(form)[1]
    source_sql_file(os.path.join(settings.OUTPUT_DIR, filename),
                    settings.DB_NAME_FINAL)


def save_dataset_as_sql(form):
    """
    Saves the dataset corresponding to *form* to the default sql dump file.
    """
    prepare_output_dir(settings.OUTPUT_DIR)
    table, file = get_sqldump_table_and_filename(form)
    dump_table_sql(settings.DB_NAME_RAW, table,
                   os.path.join(settings.OUTPUT_DIR, file))


def delete_and_create_db(db_name):
    """
    Deletes an existing database and recreates it (empty).
    """
    print("Database:", db_name)
    execute_sql("DROP DATABASE IF EXISTS {};".format(db_name))
    execute_sql("CREATE DATABASE  {0};".format(db_name))
    print("Deleted existing database and created empty database under same name.")


def import_csv(isodate, form):
    for csv_path, dbf_name in get_csv_files(isodate, form):
        mysqlimport(settings.DB_NAME_RAW, csv_path, ignore_lines=1)
    print("\nFinished importing CSV files into raw data database.")
    print("Form:", form, "Date:", isodate)


def import_csv_sqlite(isodate, form):
    """
    Temporary function to test import to sqlite database.
    Must be eventually renamed to import_csv.
    """
    for csv_path, dbf_name in get_csv_files(isodate, form):
        import_csv_to_database(form, csv_path, dbf_name)
    print("\nFinished importing CSV files into sqlite database.")
    print("Form:", form, "Date:", isodate)


def import_csv_derived_from_text_files(form):
    directory = get_private_data_folder(form, 'csv')
    for filename in os.listdir(directory):
        csv_path = os.path.join(directory, filename)
        mysqlimport(settings.DB_NAME_RAW, csv_path, ignore_lines=0)
    print("\nFinished importing CSV files into raw data database.")
    print("Directory:", directory)


def dbf2csv(isodate, form):
    """
    Converts DBF files to CSV files with SQL table name as basename and date as extension.
    This filename format allows using fast mysqlimport to read CSV files to database.
    Function will iterate over subforms in each form.
    """
    dt = iso2date(isodate)
    # Get input and output file directories
    dbf_dir = get_public_data_folder(form, 'dbf')
    csv_dir = get_public_data_folder(form, 'csv')
    # Make sure output directory exists
    if not os.path.isdir(csv_dir):
        os.makedirs(csv_dir)
    # Process all subforms in the given form.
    # For example, form 101 has two subforms: f101_B and f101B1.
    for subform, info in FORM_DATA[form].items():
        # Get DBF file (input)
        dbf_filename = make_dbf_filename(isodate, info['postfix'], form)
        dbf_path = os.path.join(dbf_dir, dbf_filename)
        if not os.path.isfile(dbf_path):
            print("File {0} not found".format(dbf_filename))
            continue
        # Get CSV file (output)
        csv_filename = make_csv_filename(dbf_filename, info['db_table'])
        print("Converting {0} to csv file {1}".format(dbf_filename, csv_filename))
        records = get_records(dbf_path, info['dbf_fields'])
        write_csv_by_path(
            records,
            os.path.join(csv_dir, csv_filename),
            info['dbf_fields'],
            form,
            dt
        )
