import datetime

from .date_engine import iso2date, zero_padded_month
from .filesystem import get_public_data_folder
from .download import download, URLError


def download_form(isodate_input, form_input):
    """
    Download archive file for specific date and form type to a local folder
    """
    url = get_url(isodate=isodate_input, form=form_input)
    dir_ = get_public_data_folder(form_input, 'rar')
    
    try:    
        download(url, dir_)
    except URLError as e:
        print('Skipping download of form {} data.\nReason: {}'.format(
            form_input, str(e)))
    
def get_url(isodate, form):
    """
    Creates URL based on date.
    """
    return "http://www.cbr.ru/credit/forms/" + get_ziprar_filename(isodate, form)

def get_ziprar_filename(isodate, form):
    """
    Returns CBR archive file name for the given form and date.
    """
    date = iso2date(isodate)

    # date is now assumed to be defined in datetime, not ISO format
    month = zero_padded_month(date.month)
    year = date.year
    extension = get_extension(date)
    
    form = str(form)
    # TODO: remove harcoded form check
    if form not in ('101', '102'):
        raise ValueError('Form {} not supported yet.'.format(form))
    return "{}-{}{}01.{}".format(form, year, month, extension)

def get_extension(date):
    # dbf files are avaialble since Feb-2004. They are in zip format up to Dec-2008
    zip_start_date = datetime.date(2004, 2, 1)
    zip_end_date = datetime.date(2008, 12, 31)

    if zip_start_date <= date <= zip_end_date:
        return 'zip'

    # dbf files are in rar format stating Jan-2009
    rar_start_date = datetime.date(2009, 1, 1)

    # rar_end_date   = datetime.datetime.now().date().replace(day=1)
    if date >= rar_start_date:
        return 'rar'
