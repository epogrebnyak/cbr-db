import os
import re
import tempfile

from cbr_db.conf import settings
from cbr_db.database.connection import get_mysql_connection, execute_sql,\
    clear_table, make_insert_statement
from cbr_db.database.process import mysqlimport_generic, mysqlimport,\
    run_sql_string, source_sql_file, dump_table_csv, dump_table_sql
from cbr_db.filesystem import prepare_output_dir, get_database_folder,\
    get_public_data_folder, get_private_data_folder
from cbr_db.terminal import terminal
from cbr_db.global_ini import DB_NAMES, ACCOUNT_NAMES_DBF, BANK_NAMES_DBF, DB_INI_DICT
from cbr_db.make_csv import list_csv_filepaths_by_date


def delete_and_create_db(db_name):
    """
    Deletes an existing database and recreates it (empty).
    """
    print("Database:", db_name)
    execute_sql("DROP DATABASE IF EXISTS {};".format(db_name))
    execute_sql("CREATE DATABASE  {0};".format(db_name))
    print("Deleted existing database and created empty database under same name.")

def get_db_dumpfile_path(db_name):
    """
    Returns the path to sql dump files, configured in DIRLIST in the
    global initialization module.
    """
    directory = get_database_folder('database')
    sql_filename = db_name + ".sql"
    path = os.path.join(directory, sql_filename).replace("\\","/")
    # path.replace(\\", '/')
    return path


def _patch_sql_file(path):
    """
    Applies necessary patches to SQL file (such as username/password).
    Returns path to patched file (in a temp folder).
    """
    with open(path, encoding='utf-8') as file:
        text = file.read()
    text = re.sub(r"([`'])\w+[`']@[`']\w+[`']",
                  r"\1{}\1@\1%\1".format(DB_INI_DICT['user']),
                  text)
    tempdir = os.path.join(tempfile.gettempdir(), 'cbr-db')
    if not os.path.isdir(tempdir):
        os.makedirs(tempdir)
    temp_file_path = os.path.join(tempdir, os.path.split(path)[1])
    with open(temp_file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return temp_file_path


def load_db_from_dump(db_name):
    """
    Loads a database structure from a dump file.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    """
    print("Database:", db_name)
    path = get_db_dumpfile_path(db_name)
    source_sql_file(_patch_sql_file(path), db_name)
    print("Loaded database structure from file <{0}.sql>. No data was imported.".format(
        db_name))


def save_db_to_dump(db_name):
    """
    Saves the structure of a database to a sql dump file in the standard location.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    # Other variety: http://code.activestate.com/recipes/286223-ohmysqldump/
    """
    print("Database:", db_name)
    # uses mysqldump and terminal()
    path = get_db_dumpfile_path(db_name)
    #               mysqldump %1  --no-data --routines > %1.sql
    line_command = "mysqldump -u{0} -p{1} {2} --no-data --routines > {3}".format(
        DB_INI_DICT['user'], DB_INI_DICT['passwd'],
        db_name, path)
    terminal(line_command)
    print("Dumped database structure to file <{0}.sql>. No data saved to this file.".format(
        db_name))


################################################################
#                  2. DBF and TXT file import                  #
################################################################

def import_csv(isodate, form):
    db_name = DB_NAMES['raw']
    for csv_path in list_csv_filepaths_by_date(isodate, form):
        mysqlimport(db_name, csv_path, ignore_lines=1)

    print("\nFinished importing CSV files into raw data database.")
    print("Form:", form, "Date:", isodate)

def import_csv_derived_from_text_files(form):
    db_name = DB_NAMES['raw']

    directory = get_private_data_folder(form, 'csv')

    for filename in os.listdir(directory):
        csv_path = os.path.join(directory, filename)
        mysqlimport(db_name, csv_path, ignore_lines=0)

    print("\nFinished importing CSV files into raw data database.")
    print("Directory:", directory)


################################################################
#              3. Dataset manipulation                         #
################################################################

def read_table_sql(db, form, file):
    """
    Support function, it is not called directly from the interface.
    todo: refactor?
    """
    prepare_output_dir(settings.OUTPUT_DIR)
    source_sql_file(os.path.join(settings.OUTPUT_DIR, file), db)


def get_sqldump_table_and_filename(form):
    """
    Returns (f101, f101.sql) for form 101, and similar output for other forms.
    Support function, it is not called directly from the interface.
    """
    table = 'f' + form
    file = table + ".sql"
    return table, file


def save_dataset_as_sql(form):
    """
    Saves the dataset corresponding to *form* to the default sql dump file.
    """
    database = DB_NAMES['raw']
    table, file = get_sqldump_table_and_filename(form)
    prepare_output_dir(settings.OUTPUT_DIR)
    dump_table_sql(database, table, os.path.join(settings.OUTPUT_DIR, file))


def import_dataset_from_sql(form):
    """
    Imports a dataset from the default sql dump file.
    """
    database = DB_NAMES['final']
    _, file = get_sqldump_table_and_filename(form)
    read_table_sql(database, form, file)






################################################################
#             4. Working with the final dataset               #
################################################################

def get_import_dbf_path(target, form):
    """
    Returns the path to the dbf file that contains the bank or account names
    for <form> to be imported to the final database. <target> can be "bank"
    (for dbf with bank names) or "plan" (for dbf with account names).

    When <target> is "plan", a single string is returned. When <target> is "bank",
    a list with two strings is returned, pointing to two distinct dbf files.
    """
    if target == "plan":
        return os.path.join(get_public_data_folder(form, 'dbf'),
                            ACCOUNT_NAMES_DBF[form])
    elif target == "bank":
        if form not in ('101', '102'):
            raise ValueError("Invalid form / form not implemented yet")
        tops = []  # two different patterns

        for pattern in BANK_NAMES_DBF:
            expr = re.compile(pattern)
            dir_ = get_public_data_folder('101', 'dbf')
            cand = []

            for file in os.listdir(dir_):
                r = expr.search(file)
                if r:
                    cand.append(r.string)

            if len(cand) == 0:
                msg = ("\n\nThere are no unpacked dbf files in {} with bank names."
                       " Did you run the commands download and unpack before?")
                raise FileNotFoundError(msg.format(dir_))

            cand.sort(key=lambda x: (x[2:6], x[0:2]), reverse=True)
            tops.append(os.path.join(dir_, cand[0]))

            return tops
    else:
        raise ValueError("Invalid target")







