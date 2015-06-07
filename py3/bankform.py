"""
Import bank sector statistics stored as archived DBF files at www.cbr.ru/credit/forms.asp to a local MySQL database, 
aggregate data into reports and dump reports to csv or xls files.

1. General database operations:      
    'save' creates database dump in <db_name>.sql file without data, unless --with-data flag is specified
    'load' imports this dump into database
    'delete' erases database
    'reset' calls 'delete' and 'load'      
   Database keywords: 
    'raw' refers to initial data database with information form DBF files (size in gigabytes)
    'final' refers to a reduced dataset used for final reports (size in 10Mb's)     
   
2. DBF file import:
    'pass' does nothing, prints date arguments to screen
    'download' saves zip/rar files form Bank of Russia web site to local folder
    'unpack' unzips/unrars DBF files
    'make csv' creates a CSV dump of DBF files     
    'import csv' reads csv files into raw database
   
3. Dataset manipulation in raw and final database:     
    'make dataset' creates a final table in raw database
    'save dataset' ...
    'import dataset' ...     
    'migrate dataset' dumps final table from raw database and imports it to final database
    
4. Working with final database:
    'import alloc' and 'import tables' read supplementary tables to final database (allocation algorithm)
    'make balance' creates table 'balance' based on 'f101', 'alloc' and supplementary tables (for form 101)
    'report balance' dumps final reporting tables to csv or xls files    
    'test balance' performs sample queries on the final reporting tables for verification purposes 

Usage:   
    bankform.py delete database (raw | final)
    bankform.py load   database (raw | final)
    bankform.py reset  database (raw | final)
    bankform.py save   database (raw | final) [--with-data]   
    
    bankform.py pass <FORM>       ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )    
    bankform.py download <FORM>   ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )    
    bankform.py make csv <FORM>   ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )    
    bankform.py unpack <FORM>     ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )    
    bankform.py make csv <FORM>   ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )    
    bankform.py import csv <FORM> ( --all-dates | --date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] )
    
    bankform.py make dataset <FORM>
    bankform.py save dataset <FORM>
    bankform.py import dataset <FORM>
    bankform.py migrate dataset <FORM>
    
    bankform.py import alloc
    bankform.py import tables    
    bankform.py make balance
    bankform.py report balance     [--csv | --xls]
    bankform.py report form <FORM> [--csv | --xls]
    bankform.py test balance

Notes:
    All dates must be in ISO format: YYYY-MM-DD
    MySQL:
        MySQL daemon must be up and running when bankform.py is started.
        Config file 'my.ini' or 'my.cfg' must contain host, user, password to allow mysql.exe calls.
        mysql*.exe must be in PATH, amend and run ini.bat
"""


from docopt import docopt
from cli_dates import get_date_range_from_command_line
from make_url import download_form
from unpack import unpack
from make_csv import dbf2csv
from global_ini import DIRLIST, DB_DICT
from global_ini import create_directories
from database import recreate_db, save_db_to_dump, load_db_from_dump, import_csv #, reset_db_from_dump
from database import save_dataset_as_sql, import_dataset_from_sql, create_final_dataset_in_raw_database
from database import import_alloc, import_tables
from database import make_balance, test_balance, report_balance_tables

EOL = "\n"
SUPPORTED_FORMS = ['101', '102', '123', '134', '135']


def get_selected_form(arg):
    form = arg["<FORM>"]
    return form if form in SUPPORTED_FORMS else None


def get_db_name(arg, db_dict=DB_DICT):
    """
    DB_DICT = {'raw': DB_NAME_RAW, "final": DB_NAME_FINAL}
    """
    # todo: shorter expression?
    db_name = None
    for param in db_dict.keys():
        if arg[param]:
            db_name = db_dict[param]
    return db_name

if __name__ == '__main__':
    arg = docopt(__doc__)
    form = get_selected_form(arg)
    date_range = get_date_range_from_command_line(arg)

    if form:
        create_directories(DIRLIST[form])

    # 1. General database operations
    if arg['database']:
        db_name = get_db_name(arg, DB_DICT)
        if arg['delete']:
            recreate_db(db_name)
        if arg['load']:
            load_db_from_dump(db_name)
        if arg['save']:
            save_db_to_dump(db_name)
        if arg['reset']:
            # EP: I suggest the following
            recreate_db(db_name)
            load_db_from_dump(db_name)
            # reset_db_from_dump(db_name)

    # 2. DBF file import
    # 'pass' option will print parsed command line arguments
    if arg['pass']:
        print("Selected form:", form)
        print("Date list:", date_range)

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

    # 3. Dataset manipulation in raw and final database
    if arg['dataset']:
        if arg['make']:
                # bankform.py make dataset <FORM>
                # Need replicate following behavior:
                # mysql --database dbf_db3 -e "call insert_f101();"
            create_final_dataset_in_raw_database()

        if arg['save']:
            save_dataset_as_sql(form)
        if arg['import']:
            import_dataset_from_sql(form)
        if arg['migrate']:
            save_dataset_as_sql(form)
            import_dataset_from_sql(form)

    # 4. Working with final database
    if arg['import'] and arg['alloc']:
        import_alloc()

    if arg['import'] and arg['tables']:
        import_tables()

    if arg['make'] and arg['balance']:
        make_balance()
        
    if arg['test'] and arg['balance']:
        test_balance()

    if arg['report'] and (arg['balance'] or arg['form']):
        report_balance_tables()
