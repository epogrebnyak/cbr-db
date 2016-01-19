import os
import re

from cbr_db.filesystem import get_public_data_folder
from cbr_db.global_ini import ACCOUNT_NAMES_DBF, BANK_NAMES_DBF


def get_import_dbf_path_for_plan(form):
    """
    Returns the path to the dbf file that contains the bank or account names
    for <form> to be imported to the final database. <target> can be "bank"
    (for dbf with bank names) or "plan" (for dbf with account names).

    When <target> is "plan", a single string is returned. When <target> is "bank",
    a list with two strings is returned, pointing to two distinct dbf files.
    """
    return os.path.join(get_public_data_folder(form, 'dbf'),
                        ACCOUNT_NAMES_DBF[form])


def get_import_dbf_path_for_bank(form):
    """
    Returns the path to the dbf file that contains the bank or account names
    for <form> to be imported to the final database. <target> can be "bank"
    (for dbf with bank names) or "plan" (for dbf with account names).

    When <target> is "plan", a single string is returned. When <target> is "bank",
    a list with two strings is returned, pointing to two distinct dbf files.
    """
    if form not in ('101', '102'):
        raise ValueError("Invalid form / form not implemented yet")
    tops = []  # two different patterns
    for pattern in BANK_NAMES_DBF:
        expr = re.compile(pattern)
        dir_ = get_public_data_folder('101', 'dbf')
        cand = []

        for file in os.listdir(dir_):
            r = expr.search(file)
            if r:
                cand.append(r.string)

        if len(cand) == 0:
            msg = ("\n\nThere are no unpacked dbf files in {} with bank names."
                   " Did you run the commands download and unpack before?")
            raise FileNotFoundError(msg.format(dir_))

        cand.sort(key=lambda x: (x[2:6], x[0:2]), reverse=True)
        tops.append(os.path.join(dir_, cand[0]))

        return tops
