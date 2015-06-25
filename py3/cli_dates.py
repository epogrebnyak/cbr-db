"""
Usage:
   new_cli.py pass <form> (<timestamp1> [<timestamp2>] | --all-dates)

   Notes:
   (1) Format for timestamps is YYYY-MM-DD (ISO), YYYY-MM, DD.MM.YYYY, MM.YYYY or YYYY
"""

from datetime import datetime, date
from docopt import docopt
from date_engine import get_date_range, shift_month_ahead

def date_from_quarter(string):
   """
   TODO:
   Add docstring here
   What is the output of function? First day of next quarter?
   """
    parts = string.upper().split('Q')
    
    if len(parts) != 2:
        return None
    else:
        # swap to year, quarter if needed
        if len(parts[0]) == 1:
            parts[0], parts[1] = parts[1], parts[0]        
        
        year, quarter = int(parts[0]), int(parts[1])
        if quarter not in range(1, 5):
            raise ValueError("Quarter must be between 1 to 4 (inclusive)")
        
        month = quarter * 3
        return shift_month_ahead(date(year=year, month=month, day=1)), "quarter"

DATE_FORMATS = ['%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']
SPECIAL_FORMATS = [date_from_quarter]

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

# TODO: 
# Comment: it would be more straight-forward under follwoing pseudocode
# Please implement
    
    # def get_date_from_monthly_timestamp(string, formats=DATE_FORMATS):
    #    same as get_date() was
    
    # def get_date_from_quarterly_timestamp(string):
    #    returns a strat-of-next-quarter date based on 1q2010, 2010Q1 format of <string>
    
    # def get_date(string)
    # if there is 'Q' in string.upper()
    #    out = get_date_from_quarterly_timestamp(string)
    # else: 
    #    out = get_date_from_monthly_timestamp(string)



def get_date(string, formats=DATE_FORMATS, special_formats=SPECIAL_FORMATS):
    """
    Tries to parse the date in string by using several predefined <formats>
    and <special_formats>.
    """
    
    for fmt in formats:
        out = try_format(string, fmt)
        if out[0]:
            return out
            
    for sp in special_formats:
        # this is very unclear fomulation below, it is hard to guess what the expression does as it involves several changes of names
        out = sp(string)
        if out[0]:
            return out

def get_last_date_in_year(dt):
    """
    Cap last month in year with current month. Returns a date with day 01.
    Example: In June 2015 will return 2015-06 for dt = 2015-12.
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
    # TODO: need to process special case when form is 102 and second time stamp is 2015 and current month is not end of quarter.
    #       get_last_date_in_year() must be sensisitve to 'form'
    if args['<timestamp2>'] is not None:
        ts2, f2 = get_date(args['<timestamp2>'])
        if f2 == "%Y":
            e = get_last_date_in_year(ts2)
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
