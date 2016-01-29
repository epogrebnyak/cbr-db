"""
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
    bankform.py update     <form> (<timestamp1> [<timestamp2>] | --all-dates)
        [--no-download]
    bankform.py import plan <form>
    bankform.py import bank
    bankform.py make csv   <form> --private-data [--all-dates]
    bankform.py import csv <form> --private-data [--all-dates]
    bankform.py make dataset <form> <timestamp1> [<timestamp2>]
        [--regn=<regn_list> | --regn-file=<file> | --regn-all]
    bankform.py save    dataset <form>
    bankform.py import  dataset <form>
    bankform.py migrate dataset <form>
    bankform.py import alloc
    bankform.py import tables
    bankform.py make   balance
    bankform.py test   balance
    bankform.py report balance     [--xlsx]
    bankform.py report form <form> [--xlsx]
"""

# todo:

# must change:
# bankform.py make csv   <form> --private-data [--all-dates]
# bankform.py import csv <form> --private-data [--all-dates]

# to:
# bankform.py make csv   <form> (<timestamp1> [<timestamp2>] | --all-dates) [--private-data]
# bankform.py import csv <form> (<timestamp1> [<timestamp2>] | --all-dates) [--private-data]

from datetime import date
import sys

from .conf import settings
from .commands import *  # NOQA
from .docopt import docopt
from .make_url import download_form
from .private_form_txt import convert_txt_directory_to_csv
from .unpack import unpack
from .utils.dates import get_date, get_next_quarter_end_date,\
    get_date_range, get_last_date_in_year

EOL = "\n"
SUPPORTED_FORMS = ['101', '102', '123', '134', '135']


def get_selected_form(arg):
    cli_form = arg["<form>"]
    return cli_form if cli_form in SUPPORTED_FORMS else None


def get_db_name(arg):
    """
    Returns a list of db names which is coded in command line by keywords 'raw' and 'final'.
    Uses dictionary DB_NAMES = {'raw': DB_NAME_RAW, "final": DB_NAME_FINAL}
    """
    db_dict = {
        'raw': settings.DB_NAME_RAW,
        'final': settings.DB_NAME_FINAL,
    }
    for param in db_dict:
        if arg[param]:
            return [db_dict[param]]
    return list(db_dict.values())


def get_date_range_from_command_line(args):
    """
    Returns date range specified in command line as a list of dates in iso format.
    """
    s, e = get_date_endpoints(args)
    step = 1
    if args['<form>'] == '102':
        step = 3
    if s and e:
        return [d.isoformat() for d in get_date_range(s, e, step)]
    else:
        return None


def get_date_endpoints(args):
    """
    Returns start and end of date range specified in command line.
    """
    start_date = None
    end_date = None
    form = args['<form>']

    if args['--all-dates']:
        # Risk: hard-coded constant
        start_date = date(2004, 2, 1)
        end_date = date.today().replace(day=1)

    # process first timestamp
    if args['<timestamp1>'] is not None:
        ts1, f1 = get_date(args['<timestamp1>'])
        start_date = ts1
        # Calculate end_date in case there is no timestamp2
        if f1 == "%Y":
            end_date = get_last_date_in_year(ts1, form)
        else:
            end_date = start_date

        if form == '102':
            # first quarter starts from month 4
            if f1 == "%Y":
                start_date = start_date.replace(month=4)

            # get current or next valid quarter
            start_date = get_next_quarter_end_date(start_date)

    # process second timestamp
    if args['<timestamp2>'] is not None:
        ts2, f2 = get_date(args['<timestamp2>'])
        if f2 == "%Y":
            end_date = get_last_date_in_year(ts2, form)
        else:
            end_date = ts2

    if start_date and end_date and (start_date.day != 1 or end_date.day != 1):
        print('Warning: must always use start of the month dates (day 1). '
              'Force setting day to 1 in argument dates.')
        start_date = start_date.replace(day=1)
        end_date = end_date.replace(day=1)

    return start_date, end_date


def main(argv):
    """
    Entry point. <argv> should contain the arguments passed to the program
    command line interface.
    """
    arg = docopt(__doc__, argv)
    form = get_selected_form(arg)
    date_range = get_date_range_from_command_line(arg)

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
            if not arg['raw']:
                import_alloc()
                import_tables()

    if arg['database']:
        db_names = get_db_name(arg)

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
            timestamp1 = date_range[0]
            timestamp2 = date_range[-1]
            regn = arg['--regn']
            regn_file = arg['--regn-file']
            regn_all = arg['--regn-all']
            create_final_dataset_in_raw_database(form, timestamp1, timestamp2,
                                                 regn, regn_file, regn_all)
        if arg['save']:
            save_dataset_as_sql(form)
        if arg['import']:
            import_dataset_from_sql(form)
        if arg['migrate']:
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
        if arg['--xlsx']:
            report_balance_tables_xls()
        else:
            report_balance_tables_csv()


if __name__ == '__main__':
    main(sys.argv[1:])
