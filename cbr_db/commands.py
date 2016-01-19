import os

from cbr_db.cli_dates import get_date
from cbr_db.utils.text import read_regn_file
from .conf import settings
from .database.api import import_records
from .database.connection import execute_sql, clear_table, insert_rows_into_table
from .database.process import mysqlimport_generic, source_sql_file, dump_table_csv, run_sql_string
from .dbftools.formats import get_import_dbf_path_for_bank, get_import_dbf_path_for_plan
from .dbftools.reader import get_records
from .filesystem import get_database_folder, get_public_data_folder, prepare_output_dir
from .global_ini import get_account_name_parameters, get_bank_name_parameters
from .make_xlsx import make_xlsx


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
    table, fields_list, dbf_fields_list = get_bank_name_parameters()

    clear_table(db, table)

    for dbf_name, fields, dbf_fields in zip(dbf_names, fields_list, dbf_fields_list):
        print("Importing bank names from {}".format(dbf_name))
        import_dbf_generic(dbf_name, db, table, fields, dbf_fields)
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
