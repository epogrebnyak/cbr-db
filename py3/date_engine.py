import datetime

def get_current_year(): 
    """
    Returns current year
    """   
    return (datetime.datetime.today().year) 

   
###########################################################
   
def date2iso(date):
    """
    Wrapper for date format conversion.
    Similar to .isoformat() method.
    """
    return datetime.date.strftime(date, "%Y-%m-%d")

def iso2date(iso_date):
    """
    Wrapper for date format conversion
    """
    return datetime.datetime.strptime(iso_date, "%Y-%m-%d").date()
        
###########################################################
    
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
    Returns date one month ahead of <date> arguement with day set to 1.
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

def get_date_range(start_date, end_date, step=1):
    """
    Returns a list with dates between <start_date> and <end_date> including end point dates.
    """  
    date_range = []
    date = start_date

    while date <= end_date:
        date_range.append(date)
        
        for s in range(step):                
            date = shift_month_ahead(date)

    return date_range    

###########################################################
    
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
    Returns a (year, quarter) tuple from a <date> object.
    Note: the first quarter corresponds to month 4, not 1.
    """
    date = shift_month_behind(date)
    return date.year, date.month // 3
    
# TODO: very awkward behaviour of  date2quarter(date) + poor docstring. Where is date2quarter() used?
   
for dt in  ("2015-01-01", "2014-12-01", "2014-11-01", "2014-10-01", "2014-09-01"):   
   print(dt, date2quarter(iso2date(dt)))

# 2015-01-01 (2014, 4) <- correct
# 2014-12-01 (2014, 3) <- incorrect
# 2014-11-01 (2014, 3) <- incorrect
# 2014-10-01 (2014, 3) <- correct
# 2014-09-01 (2014, 2) <- incorrect     

def conv_date2quarter(isodate):
    """
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
    dt = datetime.date(year=year, month=quarter * 3, day=1)
    return shift_month_ahead(dt)
    
