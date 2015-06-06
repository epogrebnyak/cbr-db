from terminal import terminal
from make_csv2 import list_csv_filepaths_by_date, mass_convert_to_csv
from cli_dates import get_date_arg_range
from form2csv import convert_subdirectories
from global_ini import DIRLIST, DIR_DBF_101, DIR_CSV_101
from make_url import download_form
from unpack import unpack_path, unpack

import docopt
import os

EOL = "\n"
FORM = ""
DB = 'dbf_db'

# Generic functions ::::::::::::::::::::::::::::::::::::::::::
def run_sql_string(string, database=None, verbose=False):
    if database is None:
        call_string = "mysql -e \"{0}\"".format(string)
    else:
        call_string = "mysql --database {0} --execute \"{1}\"".format(database, string)
    if verbose is True:
        call_string = call_string + " -v"
    terminal(call_string)

def source_db(database_name):
    string = "source {0}.sql;".format(database_name)
    run_sql_string(string, database=database_name)

def reset_database(db_name):
    command = "DROP DATABASE IF EXISTS {0};CREATE DATABASE  {0};".format(db_name)
    run_sql_string(command)

def get_db_info():
    infosting = """use dbf_db;
     select regn, count(*) as lines_total from f101 group by regn;
     select min(dt), max(dt) from f101;"""
    run_sql_string(infosting)

def run_sql_file(file, dir):
    """Runs provided file in MySQL."""
    sql_file = os.path.join(dir, file)
    call_string = "mysql < {0}".format(sql_file)
    terminal(call_string, verbose=True)

def dump_table_csv(db, table, dir):
    # function name changed
    """Saves database table in specified directory as csv file."""
    call_string = "mysqldump --fields-terminated-by=\\t\ --lines-terminated-by=\\r\\n --tab={0} {1} {2}".format(dir, db,
                                                                                                                table)
    terminal(call_string)
    # Note: below is a fix to kill unnecessary slashes in txt file.
    replace_in_file(os.path.join(dir, table + ".txt"), "\\", "")

def dump_table_sql(database, table, directory, file):
    path = os.path.join(DIRLIST[FORM]['sql'], file)
    string = "mysqldump {0} {1} --add-drop-table=FALSE --no-create-info --insert-ignore > {2}".format(database, table, path)
    terminal(string)
    # mysqldump dbf_db f101 --add-drop-table=FALSE --no-create-info --insert-ignore > %SQL_DIR%\f101.sql"""

def replace_in_file(filepath, replace_what, replace_with):
    """Replaces 'replace_what' string with 'replace_with' string in file, saves file."""
    with open(filepath) as f:
        lines = f.read().replace(replace_what, replace_with)
    with open(filepath, 'w') as f1:
        f1.write(lines)

# Functions to support command-line commands ::::::::::::::::::::::::::::::::::::::::::

def import_generic(filename, directory, mysqlimport_string):
    """Wrapper to call 'mysqlimport_string' given directory and filename of csv file with data to be imported to database"""
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        call_string = mysqlimport_string.format(path)
        terminal(call_string)
    else:
        print("File not found:", path)

def import_csv_by_filename(filename):
    import_generic(filename, DIRLIST[FORM]['csv'],
                   "mysqlimport dbf_db {0} --ignore_lines=1 --ignore ")

def import_csv(isodate, form=FORM):
    for filepath in list_csv_filepaths_by_date(isodate, form=FORM):
        import_csv_by_filename(filepath)

    # Note: possible duplicate of paths?

# Docopt ::::::::::::::::::::::::::::::::::::::::::

def get_selected_form(arg):
    selected_form = None
    for z in ['101', '102', '123', '134', '135']:
        if arg['<FORM>'] == z:
            selected_form = z
    return selected_form

def iterate_over_dates(function_name):
    arg_list = arg

    if function_name in locals():
        date_function = locals()[function_name]
    elif function_name in globals():
        date_function = globals()[function_name]

    for isodate in get_date_arg_range(arg_list):
        print(EOL + "Date:", isodate)
        date_function(isodate, form=FORM)

if __name__ == '__main__':
    arg = docopt(__doc__)
    FORM = get_selected_form(arg)
    # print(arg)

    # do nothing option - for testing
    if arg['pass'] is True:
        range = get_date_arg_range(arg)
        print(range)

    # download zip and rar files
    if arg['download'] is True:
        for isodate in get_date_arg_range(arg):
            print(EOL + "Date:", isodate)
            if arg['--test'] is True:
                download_form(isodate, form=FORM, method='test')
            else:
                download_form(isodate, form=FORM)

    # unpack dbf files
    if arg['unpack'] is True:
        if arg['--all-dates'] is True:
            # for review ----------------------
            src_dir = DIRLIST[FORM]['rar']
            dest_dir = DIRLIST[FORM]['dbf']
            for file in os.listdir(src_dir):
                filepath = os.path.join(src_dir, file)
                unpack_path(filepath, destination_directory=dest_dir)
                # end for review ----------------------
        else:
            for isodate in get_date_arg_range(arg):
                print(EOL + "Date:", isodate)
                unpack(isodate, form=FORM)

    # convert DBF to CSV
    if arg['make'] is True and arg['csv'] is True:
        if arg['extra'] is True:
            convert_subdirectories()
        if arg['--all-dates'] is True:
            # for review ----------------------
            used_file_types = ("f101_B", "f101B1")
            for file_type in used_file_types:
                # not todo+note: this is legacy call based on full directory listing, needs review
                mass_convert_to_csv(file_type, dbf_directory=DIR_DBF_101, csv_directory=DIR_CSV_101)
                # end for review ----------------------
        else:
            iterate_over_dates('dbf2csv')

    # import csv
    if arg['import'] is True and arg['csv'] is True:
        if arg['--all-dates'] is True:
            pass
        else:
            iterate_over_dates('import_csv')

    # delete and restore database structure, all existing data will be lost
    if arg["newdb"] is True:
        reset_database(DB)
        source_db(DB)

    # create form 101 in database
    if arg['build'] is True:
        # note: hardcoded 101
        run_sql_string("call insert_f101();", database=DB)
        get_db_info()

    # dump form 101 from bulk database to file
    if arg['save'] is True:
        # note: hardcoded 101
        dump_table_sql(DB, 'f101', DIRLIST[FORM]['rar'], 'f101.sql')
