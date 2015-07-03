# 
# 2015-06-19 10:27 AM
# Pandas MySQL example 
# 
# http://pandas.pydata.org/pandas-docs/stable/io.html#excel-files
# https://pandas-docs.github.io/pandas-docs-travis/generated/pandas.read_sql_table.html#pandas.read_sql_table
# 

import pandas as pd
from sqlalchemy import create_engine
from global_ini import DB_NAMES
import time

def get_sqla_connection():
    db_name = DB_NAMES['final']
    user = 'test_user'
    pwd = 'test_password'
    con = create_engine("mysql+pymysql://{0}:{1}@localhost/{2}".format(user, pwd, db_name))
    return con
    

start_time = time.time()
con = get_sqla_connection()

# Read datasets as dataframes
f101 = pd.read_sql_table('f101', con)
alloc = pd.read_sql_table('alloc', con)
balance = pd.read_sql_table('balance', con)

print("Datasets loaded in %f seconds" % (time.time() - start_time))

# Setting
# ========
# In MySQL database the 'balance' table is obtained by doing several  manipulations with 'f101' table using 'alloc' table. 
# These munipulations are performed by 'make_balance' procedure, it does 'inserts' into 'balance' table.
# 'make_balance procedure consists of three parts:
#
# call balance_make_step_1();
# call balance_make_saldo_198_298();
# call balance_make_insert_totals();
#
# Comment:
# step_1 is summation of 'f101' using 'alloc', it is the main step
# saldo_198_298 does netting of balance lines 198 and 298. temp table is created with netted lines 198 and 298 and inserted back to 'balance'
# balance_make_insert_totals adds a sum total of lines and a net of total. it inserts lines 100000, 20000 and 500 to 'balance'.

#
# Task:
# =====
# Obtain 'balance' dataframe from 'f101' and 'alloc' in pandas, 
# showing improvements in code readability over sql procedure 'make_balance'
# Prefrred results are beyond simple porting of the sql procedure. 
# 
# Data:
# =====
# Use 'py3/test-one-date.bat' to obtain for small trial dataset (one datapoint).
# Use 'py3/utils/make-reference-dataset.bat' for actual task (monthly datapoints for 2012-2015). 
#

for var in [f101, alloc, balance]:
    print()
    print(var.head())
    print(var.columns.tolist())



