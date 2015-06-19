# 
# 2015-06-19 10:27 AM
# Pandas MySQL example 
# 
# http://pandas.pydata.org/pandas-docs/stable/io.html#excel-files
# https://pandas-docs.github.io/pandas-docs-travis/generated/pandas.read_sql_table.html#pandas.read_sql_table
# 

import pandas as pd
import numpy as np
import os
from pprint import pprint
from sqlalchemy import create_engine
from global_ini import DB_NAMES
import time

def get_sqla_connection():
    db_name = DB_NAMES['final']
    user = 'test_user'
    pwd = 'test_password'
    con = create_engine("mysql+pymysql://{0}:{1}@localhost/{2}".format(user, pwd, db_name))
    return con
    

# start_time = time.time()
con = get_sqla_connection()
f101 = pd.read_sql_table('f101', con)
# print("Dataset loaded in %f seconds" % (time.time() - start_time))

print(f101.head())
pprint(f101.columns.tolist())



