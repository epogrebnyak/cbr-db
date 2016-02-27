from datetime import datetime
import os
from os import path, makedirs
import shutil
import time
from urllib.parse import urlsplit
from urllib.request import urlopen, Request

import dateutil.parser


def get_date(url):
    """
    Returns the modification date of the file pointed by *url*
    using HEAD request.
    """
    response = urlopen(Request(url, method='HEAD'))
    return dateutil.parser.parse(response.getheader('Last-Modified')).date()


def get_filename(url, dir_=""):
    """
    Returns the name of the file pointed by url, when put in directory *dir*
    """
    return path.join(dir_, path.basename(urlsplit(url).path))


def _is_already_downloaded(url, filename):
    """
    Returns True if file is already downloaded and up-to-date.
    """
    try:
        # Note: it's in local timezone
        local_date = datetime.fromtimestamp(os.path.getmtime(filename)).date()
    except FileNotFoundError:
        return False
    # To keep it simple, we just compare dates.
    return (local_date - get_date(url)).days >= 0


def download(url, dir_, force=False, verbose=True):
    """
    Downloads the file pointed by *url* into directory *dir*. Unless *force* is True,
    the file will not be downloaded if there is a local up-to-date file in *dir_*.
    """
    filename = get_filename(url, dir_)
    if _is_already_downloaded(url, filename):
        if verbose:
            print("-> Skipping {} (already downloaded)".format(url))
        return
    if verbose:
        print("-> Downloading {}".format(url))
    makedirs(dir_, exist_ok=True)
    # Download in chunks
    with urlopen(url) as response, open(filename, 'wb') as out:
        last_modified = response.getheader('Last-Modified')
        shutil.copyfileobj(response, out)
    # Set file modification time according to Last-Modified
    mtime = time.mktime(dateutil.parser.parse(last_modified).timetuple())
    os.utime(filename, (mtime, mtime))
