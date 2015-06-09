import os
from global_ini import MYSQL_PATH

def check_mysql_path():
    """
    Guarantees that the required MySQL binaries are in the PATH.
    Raises an exception if not.
    """
    # mysql is already on the PATH on Linux distros
    if os.name != 'posix':
        add_path = MYSQL_PATH.join(';')

        if add_path not in os.environ['PATH']:
            os.environ['PATH'] += ';' + add_path
            print('path updated to', os.environ['PATH'])

    # test if mysql is on the path
    if os.system('mysql -e ""') != 0:
        print("mysql is not in the PATH or the server is stopped.")
        raise AssertionError("Invalid PATH")
