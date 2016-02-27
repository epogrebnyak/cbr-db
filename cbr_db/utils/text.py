import os

from cbr_db.filesystem import get_database_folder


def replace_in_file(filepath, replace_what, replace_with):
    """
    Replaces 'replace_what' string with 'replace_with' string in filepath.
    Auxillary procedure used to clean up myslqdump csv output.
    """
    with open(filepath) as f:
        lines = f.read().replace(replace_what, replace_with)

    with open(filepath, 'w') as f1:
        f1.write(lines)


def _read_values_from_file(regn_file, sep=","):
    """
    Reads the values contained in <regn_file>, returning a list where each
    element is a list corresponding to one line of <regn_file> that was
    split using <sep>.
    """
    with open(regn_file) as f:
        data = []
        for line in f:
            data.append(line.split(sep))
        return data


def read_regn_file(regn_file):
    if not os.path.isfile(regn_file):
        path = os.path.join(get_database_folder('tables'), regn_file)
        if os.path.isfile(path):
            print('-> Using {} from {}'.format(regn_file, path))
            regn_file = path
    return _read_values_from_file(regn_file)
