"""
Usage:
   new_cli.py pass <form> (<timestamp1> [<timestamp2>] | --all-dates)

   Notes:
   (1) Format for timestamps is YYYY-MM-DD (ISO), YYYY-MM, DD.MM.YYYY, MM.YYYY or YYYY
"""

from datetime import datetime, date
from docopt import docopt
DATE_FORMATS = ['%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']

def try_format(string, format):
    """
    Attempts to parse <string> with date <format>.
    """
    z = None
    try:
        z = datetime.strptime(string, format)
        z = z.date()
    except ValueError:
        pass
    return z, format

def get_date(string, formats=DATE_FORMATS):
    """
    Applies several date <formats> to parse <string>.
    """
    for format in formats:
        z, format = try_format(string, format)
        if z is not None:
            return z, format

def get_last_date_in_year(dt):
    """
    Cap last month in year with current month. Returns a date with day 01.
    Example: In June 2015 will return 2015-06 for 2015-12.
    """
    c1 = datetime.today().replace(day=1).date()
    c2 = dt.replace(month=12)
    return min(c1, c2)

def shift_month_ahead(date_):
    """
    Shifts date to next month's day 01.
    """
    if date_.month < 12:
        date_ = date_.replace(month=date_.month + 1)
    else:
        date_ = date_.replace(month=1)
        date_ = date_.replace(year=date_.year + 1)
    return date_

def yield_date(start, end):
    """
    Yeilds dates between and including <start> and <end>.
    """
    dt = start
    while dt <= end:
        yield dt
        dt = shift_month_ahead(dt)

def get_date_range_from_command_line(args):
    """
    Returns date range specified in command line as a list of dates in iso format.
    """
    s, e = get_date_endpoints(args)
    if s is not None and e is not None:
        datelist = [x.isoformat() for x in yield_date(s, e)]
        return datelist
    else:
        return None

def get_date_endpoints(args):
    """
    Returns start and end of date range specified in command line.
    """
    s = None  # start date
    e = None  # end date

    if args['--all-dates']:
        # Risk: hard-coded constant
        s = date(2004, 2, 1)
        e = date.today().replace(day=1)

    # todo: script does not check if date is day 1. Must print warning.

    # process first timestamp
    if args['<timestamp1>'] is not None:
        ts1, f1 = get_date(args['<timestamp1>'])
        s = ts1
        if f1 == "%Y":
            e = get_last_date_in_year(ts1)
        else:
            e = s

    # process second timestamp
    if args['<timestamp2>'] is not None:
        ts2, f2 = get_date(args['<timestamp2>'])
        if f2 == "%Y":
            e = get_last_date_in_year(ts2)
        else:
            e = ts2

    return (s, e)

if __name__ == '__main__':
    args = docopt(__doc__)
    s, e = get_date_endpoints(args)
    d_range = get_date_range_from_command_line(args)
    print("Start date:", s)
    print("End date:", e)
    print("Date list:", d_range)
