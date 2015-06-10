import os
from global_ini import MYSQL_PATH

def check_mysql_path():
    """
    Guarantees that required MySQL binaries are in PATH.    
    Raises an exception if not.
    """
    # mysql is already on the PATH on Linux distros
    if os.name != 'posix':
        add_path = ';'.join(MYSQL_PATH)

        if add_path not in os.environ['PATH']:
            os.environ['PATH'] += ';' + add_path
            print('PATH updated to following:\n', os.environ['PATH'])

    # test if mysql is on the path
    if os.system('mysql -e ""') != 0:
        print("mysql.exe is not found in PATH or MySQL server not running.")
        raise AssertionError("Invalid PATH")
        
if __name__ == "__main__":
    check_mysql_path()