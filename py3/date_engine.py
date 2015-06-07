import datetime

def shift_month_ahead(date):
    if date.month < 12:
        date = date.replace(month=date.month + 1)
    else:
        date = date.replace(month=1)
        date = date.replace(year=date.year + 1)
    return(date)

def get_date_range(start_date, end_date):
    date_range = []
    date = start_date
    while date <= end_date:
        date_range.append(date)
        date = shift_month_ahead(date)
    return date_range

def get_isodate_list(start_iso_date, end_iso_date):
    range_ = get_date_range(iso2datetime(start_iso_date), iso2datetime(end_iso_date))
    return [datetime2iso(x) for x in range_]

def zero_padded_month(month):
    return "0" + str(month) if month < 10 else str(month)

def datetime2iso(date):
    return datetime.datetime.strftime(date, "%Y-%m-%d")

def iso2datetime(iso_date):
    d = datetime.datetime.strptime(iso_date, "%Y-%m-%d")
    return d.date()

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
     
    # not needed
    # if str(form) == "102":
    #    return None 

def isodate2timestamp(form, isodate):
    dt = iso2datetime(isodate)
    return date2timestamp(form, dt)

def timestamp2date(year, month=0, quarter=0):

    if month != 0 and quarter != 0:
        raise ValueError("The month and the quarter must not be specified simultaneously")

    if month == 0:
        month = (quarter - 1) * 3 + 3

    if month != 12:
        date = datetime.date(year, month + 1, 1)
    else:
        date = datetime.date(year + 1, 1, 1)

    return date

def year_start_isodate(year):
    return datetime2iso(datetime.date(int(year), 1, 1))

def year_end_isodate(year):
    current = datetime.date.today().replace(day=1)
    input_ = datetime.date(int(year), 12, 1)

    if input_ > current:
        res = current
    else:
        res = input_

    return res.isoformat()

def this_month_isodate():
    res = datetime.date.today().replace(day=1)
    return res.isoformat()

def is_isodate(isodate):
    # todo - does not catch error ValueError, e.g. in  is_isodate("2015-01-01"):
    # check format for date YYYY-MM-DD
    # check if date makes sense
    try:
        around_value = iso2datetime(isodate).isoformat()
        return around_value == isodate
    except ValueError:
        return False

def check_isodate(isodate):
    if not is_isodate(isodate):
        raise ValueError("date {} is not in the ISO format".format(isodate))
    else:
        return isodate
