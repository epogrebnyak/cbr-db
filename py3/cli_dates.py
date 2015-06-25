"""
Usage:
   cli_dates.py pass <form> (<timestamp1> [<timestamp2>] | --all-dates)

   Notes:
   (1) Format for timestamps is YYYY-MM-DD (ISO), YYYY-MM, DD.MM.YYYY, MM.YYYY or YYYY
"""

from datetime import datetime, date
from docopt import docopt
from date_engine import get_date_range, shift_month_ahead

def get_date_from_quarter_string(string):
    """
    Returns a date object from a <string> describing a date using a quarter
    notation, like 1Q2005, 4q2003, 2003Q3 or 2003q2.
    """
    # break into year, quarter or quarter, year
    parts = string.upper().split('Q')
    
    if len(parts) != 2:
        # not in a quarter format, break
        return None
    else:
        # make sure the order is year, quater
        if len(parts[0]) == 1:
            parts[0], parts[1] = parts[1], parts[0]        
        
        # convert to integer checking the range
        year, quarter = int(parts[0]), int(parts[1])
        if quarter not in range(1, 5):
            raise ValueError("Quarter must be between 1 to 4 (inclusive)")
        
        # first quarter: month 4. last quarter: first month of next year
        month = quarter * 3
        dt = date(year=year, month=month, day=1)
        return shift_month_ahead(dt), "quarter"

# new formatters can be added by appending to DATE_FORMATS (text patterns) and
# to SPECIAL_FORMATS (functions that accepts one string argument)
DATE_FORMATS = ['%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']
SPECIAL_FORMATS = [get_date_from_quarter_string]

def try_format(string, fmt):
    """
    Attempts to parse <string> with date <fmt> (format).
    """
    z = None
    try:
        z = datetime.strptime(string, fmt)
        z = z.date()
    except ValueError:
        pass

    return z, fmt

def get_date(string, formats=DATE_FORMATS, special_formats=SPECIAL_FORMATS):
    """
    Tries to parse the date in string by using several predefined <formats>
    and <special_formats>.
    """
    
    # tries the pattern formats one by one up to the first that parses the date
    for fmt in formats:
        parse_output = try_format(string, fmt)
        if parse_output[0]: return parse_output
        
    # tries the special formats one by one, same as above
    for special_format in special_formats:
        parse_output = special_format(string)
        if parse_output[0]: return parse_output
            
def get_last_quarter_month(month):
    """
    Returns the last completed quarter from <month>.
    Note: returns month 1, 4 or 7 or 10.
    """
    quarter = (month - 1) // 3
    return quarter * 3 + 1

def get_last_date_in_year(dt, form):
    """
    Cap last month in year with current month. Returns a date with day 01.
    Example: In June 2015 will return 2015-06 for dt = 2015-12.
    In forms with quarter notation, returns the last valid quarter.
    """
    c1 = datetime.today().replace(day=1).date()
    c2 = dt.replace(month=12)
    dt = min(c1, c2)
            
    if form == '102': # quarter notation
        if c2 == dt:
            # we can get the end of the 4º quarter that is in the next year
            dt = dt.replace(year=dt.year+1, month=1)
        else:
            # go back to the last valid quarter
            dt = dt.replace(month=get_last_quarter_month(dt.month))
    else:
        raise ValueError('Form {} is not supported yet.'.format(form))
    
    return dt

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
            e = get_last_date_in_year(ts1, args['<form>'])
        else:
            e = s

    # process second timestamp
    if args['<timestamp2>'] is not None:
        ts2, f2 = get_date(args['<timestamp2>'])
        if f2 == "%Y":
            e = get_last_date_in_year(ts2, args['<form>'])
        else:
            e = ts2

    if s and e and (s.day != 1 or e.day != 1):
        print('Warning: must always use start of the month dates (day 1). Force setting day to 1 in argument dates.')
        s = s.replace(day=1)
        e = e.replace(day=1)

    return s, e

if __name__ == '__main__':
    args = docopt(__doc__)
    d_range = get_date_range_from_command_line(args)
    print("Start date:", d_range[0])
    print("End date:",   d_range[-1])
    print("Date list:",  d_range)
