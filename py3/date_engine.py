import datetime

def _verify_start_of_month(*args):
    for date in args:
        if date.day != 1:
            raise ValueError("All dates must be at the start of the month (day 1)")
            
def date2iso(date):
    return datetime.date.strftime(date, "%Y-%m-%d")

def iso2date(iso_date):
    return datetime.datetime.strptime(iso_date, "%Y-%m-%d").date()

def shift_month_ahead(date):
    _verify_start_of_month(date)

    if date.month < 12:
        date = date.replace(month=date.month + 1)
    else:
        date = date.replace(month=1)
        date = date.replace(year=date.year + 1)

    return date

def get_date_range(start_date, end_date):
    """
    Returns a list with dates between (and including) <start_date> and <end_date>.
    """
    _verify_start_of_month(start_date, end_date)

    date_range = []
    date = start_date

    while date <= end_date:
        date_range.append(date)
        date = shift_month_ahead(date)

    return date_range

def zero_padded_month(month):
    return "0" + str(month) if month < 10 else str(month)

def date2timestamp(form, dt):
    # must keet this hardcoded, different code will apply to different form
    if str(form) == "101":
        if dt.month == 1:
            year = dt.year - 1
            month = 12
        else:
            year = dt.year
            month = dt.month - 1

        return zero_padded_month(month) + str(year)

def isodate2timestamp(form, isodate):
    dt = iso2date(isodate)
    return date2timestamp(form, dt)
