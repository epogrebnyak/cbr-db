import datetime
import sys
from date_engine import iso2datetime, zero_padded_month
from global_ini import DIRLIST
from download import download

def download_form(isodate_input, form_input):
    """
    Download archive file for specific date and form type to a local folder
    """
    url = get_url(isodate=isodate_input, form=form_input)
    dir_ = DIRLIST[form_input]['rar']
    download(url, dir_)

def get_url(date=None, isodate=None, form=None):
    """
    Creates URL based on date for form 101
    """
    if form == '101':
        url = "http://www.cbr.ru/credit/forms/" + get_ziprar_filename(date, isodate, form)        
    return url

def get_ziprar_filename(date=None, isodate=None, form=None):
    if isodate is not None:
        date = iso2datetime(isodate)
    elif date is None:
        return None

    # date is now assumed to be defined in datetime, not ISO format
    month = zero_padded_month(date.month)
    year = date.year
    extension = get_extension(date)

    if form == '101':
        return "101-{0}{1}01.{2}".format(year, month, extension)
    

def get_extension(date):
    # dbf files are avaialble since Feb-2004. They are in zip format up to Dec-2008
    zip_start_date = datetime.date(2004, 2, 1)
    zip_end_date = datetime.date(2008, 12, 1)

    extension = None  # prevents extension from not being set if rar_start_date or zip_end_date changes
    if zip_start_date <= date <= zip_end_date:
        extension = 'zip'

    # dbf files are in rar format stating Jan-2009
    rar_start_date = datetime.date(2009, 1, 1)

    # rar_end_date   = datetime.datetime.now().date().replace(day=1)
    if date >= rar_start_date:
        extension = 'rar'

    return extension

if __name__ == "__main__":
    if len(sys.argv) == 1:
        date_floor = None
        date_most_recent = None
    elif len(sys.argv) == 3:
        date_floor = sys.argv[1]
        date_most_recent = sys.argv[2]
    else:
        raise ValueError("Must have none or two parameters YYYY-MM-DD YYYY-MM-DD")
