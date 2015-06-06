import os

def check_mysql_path():
    """
    Guarantees that the required MySQL binaries are in the PATH.
    Raises an exception if not.
    """
    # mysql is already on the PATH on Linux distros
    if os.name != 'posix':
        os.environ['PATH'] += ';C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin'
        print('path: ', os.environ['PATH'])

    # test if mysql is on the path
    if os.system('mysql -e ""') != 0:
        print("mysql is not in the PATH or the server is stopped.")
        raise AssertionError("Invalid PATH")
