import os
from terminal import terminal
from global_ini import PATH, DIRLIST
from make_url import get_ziprar_filename

def get_local_ziprar_filepath(isodate, form):
    dir_ = DIRLIST[form]['rar']
    filename = get_ziprar_filename(isodate=isodate, form=form)
    print("File:", filename)
    return os.path.join(dir_, filename)

def unpack(isodate, form):
    # not todo - may omit 'destination_directory' form here
    filepath = get_local_ziprar_filepath(isodate, form)
    unpack_path(filepath, form)

def unpack_path(filepath, form):
    destination_directory = DIRLIST[form]['dbf']
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.rar':
        call_string = " ".join([in_quotes(PATH['unrar']), "e", filepath, destination_directory, "-y"])
    else:
        call_string = " ".join([in_quotes(PATH['z7']), "e", filepath, "-o" + destination_directory, "-y"])

    terminal(call_string)

def in_quotes(str):
    return '"' + str + '"'
