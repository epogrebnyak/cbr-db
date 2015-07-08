"""
Import bank sector statistics stored as archived DBF files at www.cbr.ru/credit/forms.asp to a local MySQL database, aggregate data into reports and save reports in csv or xlsx format. The script can also import statistics stored locally in text form files ("private data").

1. General database operations:
    'save' creates database dump in <db_name>.sql file without data, unless --with-data flag is specified
    'load' imports this dump into database
    'delete' erases database
    'reset' calls 'delete' and 'load'
   Database keywords:
    'raw' refers to initial data database with information form DBF files (size in gigabytes)
    'final' refers to a reduced dataset used for final reports (size in 10Mb's)

2. DBF/TXT file import
2.1. Public data (DBF files as source)
    'download' saves zip/rar files form Bank of Russia web site to local folder
    'unpack' unzips/unrars DBF files
    'make csv' creates a CSV dump of DBF files
    'import csv' reads csv files into raw database
2.2. Private data (TXT files as source)
    'make csv' converts text files to csv
    'import csv' reads csv files into raw database
    Note: no timestamps for private data are used, all files are processed.

3. Dataset manipulation in raw and final database:
    'make dataset' creates a final table in raw database
    'save dataset' ... # todo: as in docstrings
    'import dataset' ... # todo: as in docstrings
    'migrate dataset' dumps final table from raw database and imports it to final database

4. Working with final database:
    'import plan' reads account names into final database
    'import alloc' and 'import tables' read supplementary tables to final database (allocation algorithm)
    'make balance' creates table 'balance' based on 'f101', 'alloc' and supplementary tables (for form 101)
    'report balance' dumps final reporting tables to csv or xls files
    'test balance' performs sample queries on the final reporting tables for verification purposes

Usage:
    bankform.py save    database [raw | final]
    bankform.py delete  database [raw | final]
    bankform.py load    database [raw | final]
    bankform.py reset   database [raw | final]
    bankform.py download   <form> (<timestamp1> [<timestamp2>] | --all-dates)
    bankform.py make csv   <form> (<timestamp1> [<timestamp2>] | --all-dates)
    bankform.py unpack     <form> (<timestamp1> [<timestamp2>] | --all-dates)
    bankform.py make csv   <form> (<timestamp1> [<timestamp2>] | --all-dates)
    bankform.py import csv <form> (<timestamp1> [<timestamp2>] | --all-dates)
    bankform.py import plan <form>
    bankform.py import bank
    bankform.py update     <form> (<timestamp1> [<timestamp2>] | --all-dates) [--no-download]
    bankform.py make csv   <form> --private-data [--all-dates]
    bankform.py import csv <form> --private-data [--all-dates]
    bankform.py make dataset <form> <timestamp1> [<timestamp2>] [--regn=<regn_list> | --regn-file=<file> | --regn-all]
    bankform.py save    dataset <form>
    bankform.py import  dataset <form>
    bankform.py migrate dataset <form>
    bankform.py import alloc
    bankform.py import tables
    bankform.py make   balance
    bankform.py test   balance
    bankform.py report balance     [--xlsx]
    bankform.py report form <form> [--xlsx]

Notes:
    (1) Format for timestamps is YYYY-MM-DD (ISO), YYYY-MM, DD.MM.YYYY, MM.YYYY or YYYY
    MySQL configuration requirements:
        MySQL server daemon must be up and running when bankform.py is started.
        Config file 'my.ini' or 'my.cfg' must contain host, user, password to allow mysql.exe calls.
        mysql*.exe must be in PATH. If not in PATH run utils\ini.bat or utils\ini.py with correct path to mysql.
"""

from docopt import docopt
from cli_dates import get_date_range_from_command_line
from make_url import download_form
from unpack import unpack
from make_csv import dbf2csv
from global_ini import DB_NAMES, create_default_directories
from database import delete_and_create_db, save_db_to_dump, load_db_from_dump
from database import import_csv, import_csv_derived_from_text_files
from private_form_txt import convert_txt_directory_to_csv
from database import save_dataset_as_sql, import_dataset_from_sql, create_final_dataset_in_raw_database
from database import import_alloc, import_tables, import_plan, import_bank
from database import make_balance, test_balance, report_balance_tables_csv, report_balance_tables_xls
import sys

EOL = "\n"
SUPPORTED_FORMS = ['101', '102', '123', '134', '135']


def get_selected_form(arg):    
    cli_form = arg["<form>"]
    return cli_form if cli_form in SUPPORTED_FORMS else None


def get_db_name(arg, db_dict=DB_NAMES):
    """
    Returns a list of db names which is coded in command line by keywords 'raw' and 'final'.
    Uses global dictionary DB_NAMES = {'raw': DB_NAME_RAW, "final": DB_NAME_FINAL}
    """
    for param in db_dict:
        if arg[param]:
            return [db_dict[param]]

    return list(db_dict.values())

def main(argv):
    """
    Entry point. <argv> should contain the arguments passed to the program
    command line interface.
    """
    arg = docopt(__doc__, argv)
    form = get_selected_form(arg)
    date_range = get_date_range_from_command_line(arg)
    
    create_default_directories()

    # 1. General database operations
    def general_database_operations(arg, db_name):
        if arg['delete']:
            delete_and_create_db(db_name)
        if arg['load']:
            load_db_from_dump(db_name)
        if arg['save']:
            save_db_to_dump(db_name)
        if arg['reset']:
            delete_and_create_db(db_name)
            load_db_from_dump(db_name)
            if arg['final']:
                import_alloc()
                import_tables()

    if arg['database']:
        db_names = get_db_name(arg, DB_NAMES)

        for db_name in db_names:
                general_database_operations(arg, db_name)

    # 2.1 DBF file import

    if date_range is not None:
        for isodate in date_range:

            print(EOL + "Date:", isodate)

            # download zip and rar files
            if arg['download']:
                download_form(isodate, form)

            # unzip/unrar downloaded files
            if arg['unpack']:
                unpack(isodate, form)

            # convert DBF to CSV
            if arg['make'] and arg['csv']:
                dbf2csv(isodate, form)

            # import CSV for selected dates into raw database
            if arg['import'] and arg['csv']:
                import_csv(isodate, form)

            # do all data import operations
            if arg['update']:
                if not arg['--no-download']:
                   download_form(isodate, form)                   
                unpack(isodate, form)
                dbf2csv(isodate, form)
                import_csv(isodate, form)

    # 2.2 Text file import
    if arg["--private-data"]:
            # convert text to CSV
            if arg['make'] and arg['csv']:
                convert_txt_directory_to_csv(form)

            # import CSV into raw database
            if arg['import'] and arg['csv']:
                import_csv_derived_from_text_files(form)

    # 3. Dataset manipulation in raw and final database
    if arg['dataset']:
        if arg['make']:
            timestamp1 = arg.get('<timestamp1>')
            timestamp2 = arg.get('<timestamp2>')
            regn = arg.get('--regn')
            regn_file = arg.get('--regn-file')
            regn_all = arg.get('--regn-all')
            create_final_dataset_in_raw_database(form, timestamp1, timestamp2,
                                                 regn, regn_file, regn_all)

        if arg['save']:
            save_dataset_as_sql(form)
        if arg['import']:
            import_dataset_from_sql(form)
        if arg['migrate']:
            #create_final_dataset_in_raw_database(form) # was called again!
            save_dataset_as_sql(form)
            import_dataset_from_sql(form)

    # 4. Working with final database
    if arg['import'] and arg['plan']:
        import_plan(form)
        
    if arg['import'] and arg['bank']:
        import_bank()

    if arg['import'] and arg['alloc']:
        import_alloc()

    if arg['import'] and arg['tables']:
        import_tables()

    if arg['make'] and arg['balance']:
        make_balance()

    if arg['test'] and arg['balance']:
        test_balance()

    if arg['report'] and (arg['balance'] or arg['form']):
        report_balance_tables_csv()
        if arg['--xlsx']:
            report_balance_tables_xls()


if __name__ == '__main__':
    main(sys.argv[1:])