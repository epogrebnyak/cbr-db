import os
from zipfile import ZipFile

from .conf import settings
from .terminal import terminal
from .config_folders import get_public_data_folder
from .make_url import get_ziprar_filename


def get_local_ziprar_filepath(isodate, form):
    dir_ = get_public_data_folder(form, 'rar')
    filename = get_ziprar_filename(isodate=isodate, form=form)
    print("File:", filename)
    return os.path.join(dir_, filename)


def unpack(isodate, form):
    # not todo - may omit 'destination_directory' form here
    filepath = get_local_ziprar_filepath(isodate, form)
    unpack_path(filepath, form)


def unpack_path(filepath, form):
    destination_directory = get_public_data_folder(form, 'dbf')
    ext = os.path.splitext(filepath)[1].lstrip('.').lower()
    # Make sure target directory exists.
    # NOTE: `unrar e` may do nothing if target directory does not exist.
    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)
    if ext == 'rar':
        _unpack_rar(filepath, destination_directory)
    elif ext == 'zip':
        _unpack_zip(filepath, destination_directory)
    elif ext == '7z':
        _unpack_7z(filepath, destination_directory)
    else:
        raise Exception('Unsupported archive type: {}'.format(filepath))


def _unpack_rar(filepath, destination_dir):
    call_string = " ".join([in_quotes(settings.UNPACK_RAR_EXE), "e", filepath, destination_dir, "-y"])
    terminal(call_string)


def _unpack_zip(filepath, destination_dir):
    with ZipFile(filepath, 'r') as file:
        file.extractall(destination_dir)


# TODO: not sure there are actual 7z - maybe we don't need this
def _unpack_7z(filepath, destination_dir):
    call_string = " ".join([in_quotes(settings.UNPACK_7Z_EXE), "e", filepath, "-o" + destination_dir, "-y"])
    terminal(call_string)


def in_quotes(str):
    return '"' + str + '"'
