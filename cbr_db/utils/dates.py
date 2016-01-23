"""
This module contains functions to process datetime strings and objects.
"""

from datetime import date, datetime


def _verify_start_of_month(*args):
    """
    Checks if day of date is 01, raises error otherwise.
    Note: this is now a double check as cli_dates.get_date_endpoints() forces day to 1, occurrence of other day is unlikely.
    """
    for date in args:
        if date.day != 1:
            raise ValueError("All dates must be at the start of the month (day 1)")


def shift_month_ahead(date):
    """
    Returns date one month ahead of <date> argument with day set to 1.
    """
    _verify_start_of_month(date)

    if date.month < 12:
        date = date.replace(month=date.month + 1)
    else:
        date = date.replace(month=1)
        date = date.replace(year=date.year + 1)

    return date


def shift_month_behind(date):
    """
    Returns date one month behind of <date> arguement with day set to 1.
    """
    _verify_start_of_month(date)

    if date.month > 1:
        date = date.replace(month=date.month - 1)
    else:
        date = date.replace(month=12)
        date = date.replace(year=date.year - 1)

    return date


def shift_month_to_quarter_start(month):
    """
    Shifts <month> to start of quarter. Function used to obtain valid quarter reporting date.
    Always returns 1, 4, 7 or 10:
    month | result
    1 1
    2 1
    3 1
    4 4
    5 4
    6 4
    7 7
    8 7
    9 7
    10 10
    11 10
    12 10
    """
    # Note: former name 'get_last_quarter_month' contradicted function algorithm.
    #"""
    #Returns the last completed quarter from <month>. For example, if the
    #month is 1, 2 or 3, the last completed quarter was at month 1.
    #Note: always returns month 1, 4, 7 or 10.
    #"""
    quarter = (month - 1) // 3
    return quarter * 3 + 1


def get_date_range(start_date, end_date, step=1):
    """
    Returns a list with dates between <start_date> and <end_date> including end point dates.
    """
    date_range = []
    date = start_date
    # Generate dates with the given step
    while date <= end_date:
        date_range.append(date)
        # Step N months forward
        for s in range(step):
            date = shift_month_ahead(date)
    return date_range


def get_date_from_quarter_string(timestamp):
    """
    Returns day 1 of quarter following <timestamp> argument.
    Example: for timestamp = '1q2015' returns date object with date '2015-04-01'
    <timestamp describes a date using a quarter-year  notation [1-4]q[YYYY], [1-4]Q[YYYY], [YYYY]q[1-4], [YYYY]Q[1-4]
    <timestamp> examples: 1Q2005, 2q2005, 2005Q3, 2005q4
    """
    # not todo: may use regex to catch year/quarter

    # break into (year, quarter) or (quarter, year)
    parts = timestamp.upper().split('Q')

    if len(parts) != 2:
        # not in a quarter format, break
        return None
    else:
        # make sure the order is (year, quater), swap to this format if otherwise
        if len(parts[0]) == 1:
            parts[0], parts[1] = parts[1], parts[0]

        # convert to integer checking the range
        year, quarter = int(parts[0]), int(parts[1])
        if quarter not in range(1, 5):
            raise ValueError("Quarter must be 1, 2, 3 or 4")

        # first quarter: month 4. last quarter: first month of next year
        month = quarter * 3
        dt = date(year=year, month=month, day=1)
        return shift_month_ahead(dt), "quarter"


_DATE_FORMATS = ['%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']
_SPECIAL_FORMATS = [get_date_from_quarter_string]


def get_date(string):
    """
    Parses <string> as date using several predefined text <formats> and <special_formats> functions,
    returning the date and the its matching format.
    """

    # tries the pattern formats one by one up to the first that parses the date
    for fmt in _DATE_FORMATS:
        try:
            return (datetime.strptime(string, fmt).date(), fmt)
        except ValueError:
            pass

    # tries the special formats one by one, same as above. special_format is a function.
    for special_format in _SPECIAL_FORMATS:
        parse_output = special_format(string)
        if parse_output[0]:
            return parse_output


def get_current_year():
    """
    Returns current year
    """
    return (datetime.today().year)


def date2iso(date):
    """
    Wrapper for date format conversion.
    Similar to .isoformat() method.
    """
    return date.strftime("%Y-%m-%d")


def iso2date(iso_date):
    """
    Wrapper for date format conversion
    """
    return datetime.strptime(iso_date, "%Y-%m-%d").date()


def isodate2timestamp(form, isodate):
    """
    Returns timestamp string used in <form> filenames based on <isodate> argument.
    """
    dt = iso2date(isodate)
    return date2timestamp(form, dt)


def date2timestamp(form, dt):
    """
    Returns timestamp string used in <form> filenames based on <dt> argument.
    """
    form = str(form)

    # Risk: must keet this hardcoded, different code will apply to different <form>
    if form == "101":
        # filename timestamp is one month behind
        if dt.month == 1:
            year = dt.year - 1
            month = 12
        else:
            year = dt.year
            month = dt.month - 1
        return zero_padded_month(month) + str(year)
    elif form == '102':
        # deals in quarters
        year, quarter = date2quarter(dt)
        return "{}{}".format(quarter, year)
    else:
        raise ValueError("Form not supported: " + form)


def zero_padded_month(month):
    """
    Returns 01, 02, ... 10, 11, 12.
    """
    return "0" + str(month) if month < 10 else str(month)


def date2quarter(date):
    """
    Returns the last completed quarter (year, quarter) tuple from a <date> object (a reverse quarter2date).
    The function expects a valid end-of-quarter month (months 1, 4, 7, 10) .
    """
    if date.month == 1:
        return (date.year - 1, 4)
    elif date.month in (4, 7, 10):
        return (date.year, (date.month - 1) // 3)
    else:
        raise ValueError("Month {} does is not a end-of-quarter month (months 1, 4, 7, and 10)")


def conv_date2quarter(isodate):
    """
    Returns year and quarter which correspond to reporting <isodate>
    """
    date = iso2date(isodate)
    date = shift_month_behind(date)
    mo2qtr = {1:1, 2:1, 3:1,
              4:2, 5:2, 6:2,
              7:3, 8:3, 9:3,
             10:4, 11:4, 12:4}
    return date.year, mo2qtr[date.month]


def quarter2date(year, quarter):
    """
    Returns reporting date from <year> and <quarter>.
    Reporting date is day of month following the quarter.
    E.g. for quarter = 1 and year = 2014 reporting date is 2014-04-01
    """
    dt = date(year=year, month=quarter * 3, day=1)
    return shift_month_ahead(dt)


def get_next_quarter_end_date(dt):
    """
    Returns the date corresponding to the next quarter end from <dt>.
    For example, if the current month is 1, it is currently in a valid
    quarter end. Months 2 and 3 would be changed to 4.
    """
    while (dt.month - 1) % 3 != 0:
        dt = shift_month_ahead(dt)
    return dt


def get_last_date_in_year(dt, form):
    """
    Cap last month in year with current month. Returns a date with day 01.
    Example: In June 2015 will return 2015-06 for dt = 2015-12.
    In forms with quarter notation, returns the last valid quarter.
    """
    current_month_day_1 = date.today().replace(day=1)
    current_year_dec1_date = dt.replace(month=12)
    dt = min(current_month_day_1, current_year_dec1_date)

    if form == '102':  # use quarter notation
        if current_year_dec1_date == dt:
            # we can get the end of the 4 quarter that is in the next year
            dt = dt.replace(year=dt.year + 1, month=1)
        else:
            # go back to the last valid quarter reporting date
            dt = dt.replace(month=shift_month_to_quarter_start(dt.month))

    return dt
