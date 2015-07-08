import pymysql
from global_ini import CODEPAGE

DB_INI_DICT = {'host': 'localhost', 'port':3306, 'user':'test_user', 'passwd':'test_password'}

def get_mysql_connection(credential_dict=DB_INI_DICT, database=None, autocommit=False,
                         charset=CODEPAGE):
    # todo: add try-except raise 
    #       maybe can add arg unpacking     
    if database is None:
        conn = pymysql.connect(host=credential_dict['host'], port=credential_dict['port'], 
                               user=credential_dict['user'], passwd=credential_dict['passwd'],
                               autocommit=autocommit, charset=charset)
    else:
        conn = pymysql.connect(host=credential_dict['host'], port=credential_dict['port'], 
                               user=credential_dict['user'], passwd=credential_dict['passwd'],
                               db=database, autocommit=autocommit, charset=charset)
    return conn                         
 

def execute_sql_with_cursor(sql_string, cur, verbose=False):
    """
    Executes a SQL query with an existing cursor, returning all the
    results (if any).
    """
    cur.execute(sql_string)
    
    if verbose is True:
        print(cur.description)
    
    return cur.fetchall()

def execute_sql(sql_string, database=None, verbose=False):
    """
    Executes a SQL query, returning all the results. A new connection is
    opened and closed at every call by using the default credentials.
    """
    conn = get_mysql_connection (DB_INI_DICT, database)
    cur = conn.cursor()
    resp = execute_sql_with_cursor(sql_string, cur, verbose)    
    conn.commit()
    cur.close()
    conn.close()
    
    return resp