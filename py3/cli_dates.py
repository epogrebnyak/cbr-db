"""
Usage:
   new_cli.py pass <form> (<timestamp1> [<timestamp2>] | --all-dates)

   Notes:
   (1) Format for timestamps is YYYY-MM-DD (ISO), YYYY-MM, DD.MM.YYYY, MM.YYYY or YYYY
"""

from datetime import datetime, date
from docopt import docopt
from date_engine import get_date_range
DATE_FORMATS = ['%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']

def try_format(string, fmt):
    """
    Attempts to parse <string> with date <format>.
    """
    z = None
    try:
        z = datetime.strptime(string, fmt)
        z = z.date()
    except ValueError:
        pass

    return z, fmt

def get_date(string, formats=DATE_FORMATS):
    """
    Applies several date <formats> to parse <string>.
    """
    for fmt in formats:
        z, fmt = try_format(string, fmt)

        if z:
            return z, fmt

def get_last_date_in_year(dt):
    """
    Cap last month in year with current month. Returns a date with day 01.
    Example: In June 2015 will return 2015-06 for 2015-12.
    """
    c1 = datetime.today().replace(day=1).date()
    c2 = dt.replace(month=12)
    return min(c1, c2)

def get_date_range_from_command_line(args):
    """
    Returns date range specified in command line as a list of dates in iso format.
    """
    s, e = get_date_endpoints(args)

    if s and e:
        return [d.isoformat() for d in get_date_range(s, e)]

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

    if s and e and (s.day != 1 or e.day != 1):
        print('Warning: must always use dates in the start of the month (day 1). Forcing day=1.')
        s = s.replace(day=1)
        e = e.replace(day=1)

    return s, e

if __name__ == '__main__':
    args = docopt(__doc__)
    d_range = get_date_range_from_command_line(args)
    print("Start date:", d_range[0])
    print("End date:", d_range[-1])
    print("Date list:", d_range)
