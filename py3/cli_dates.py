"""Usage:
   cli_dates2.py pass <FORM> (--date <date> | --date-start <date_start> [--date-end <date_end>] | --year <year> | --year-start <year_start> [--year-end <year_end>] | --all-dates )
   cli_dates2.py pass
   cli_dates2.py pass <FORM> --all-dates
   cli_dates2.py pass <FORM> --date <date>
   cli_dates2.py pass <FORM> --date-start <date_start> [--date-end <date_end>]
   cli_dates2.py pass <FORM> --year <year>
   cli_dates2.py pass <FORM> --year-start <year_start> [--year-end <year_end>]
   cli_dates2.py pass <form> [<timestamp1> [<timestamp2>]] [--all-dates]

   Notes:
   (1) Format for all dates is YYYY-MM-DD (ISO)"""

import date_engine

def get_date_range_from_command_line_as_datetime(arg):
    """
    Оutput of get_date_range_from_command_line(arg) in datetime format.
    """
    iso_date_list = get_date_range_from_command_line(arg)
    datetime_date_list = [date_engine.iso2datetime(x) for x in iso_date_list]
    return datetime_date_list

def get_date_range_from_command_line(arg):
    """
    Transforms command line arguments to a list of dates in ISO format (default) of datetime format.
    Example: ["2015-01-01", "2015-02-01"]
    """
    s = None  # start iso date
    e = None  # end iso date

    if arg['--date-start']:
        s = date_engine.check_isodate(arg['<date_start>'])
        # if end date not supplied make it today
        if arg['--date-end']:
            e = date_engine.check_isodate(arg['<date_end>'])
        else:
            e = date_engine.this_month_isodate()
    elif arg['--year']:
        s = date_engine.year_start_isodate(arg['<year>'])
        e = date_engine.year_end_isodate(arg['<year>'])
    elif arg['--year-start']:
        # make s start of year 1-Jan
        s = date_engine.year_start_isodate(arg['<year_start>'])
        # make end of year 1-Dec year or current month start, whichever earlier
        if arg['--year-end']:
            e = date_engine.year_end_isodate(arg['<year_end>'])
        else:
            e = date_engine.year_end_isodate(arg['<year_start>'])
    elif arg['--date']:
        # check format for date YYYY-MM-DD or YYYY-DD
        # check if date makes sense
        s = date_engine.check_isodate(arg['<date>'])
        e = s
    elif arg['--all-dates']:
        # L: where is DATE_FLOOR_ISO defined?
        s = date_engine.check_isodate(DATE_FLOOR_ISO)
        e = date_engine.this_month_isodate()

    if s is None or e is None:
        return None

    return date_engine.get_isodate_list(s, e)

if __name__ == '__main__':

    from docopt import docopt
    arg = docopt(__doc__)

    # do nothing option - for testing
    if arg['pass']:
        range1 = get_date_range_from_command_line(arg)
        print(range1)
        range2 = get_date_range_from_command_line_as_datetime(arg)
        print(range2)
