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

#balance_make_step_1():
#===========================
# CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make_step_1`()
# BEGIN
#
#     drop table if exists balance;
#
#     create table if not exists balance as
#     SELECT  dt, line,
#             lev, la_p,
#             regn,
#             has_iv,
#             sum(   ir*mult) ir,
#             sum(   iv*mult) iv,
#             sum(itogo*mult) itogo
#     from alloc a left join f101 v on v.conto = a.conto
#     where v.conto Is not null
#     group by dt, line, regn;
#
#     create index bal_index_1 on balance (line, regn, dt);
#
# END ;;

balancedf = alloc.merge(f101, on='conto', how='left')
#TODO: check if v.conto is null, if yes then drop those rows, need some data in tables for this
balancedf = balancedf.ix[:,['dt', 'line', 'lev', 'la_p', 'regn', 'has_iv', 'ir', 'iv', 'itogo']]
#TODO: continue with groupby implementation

#balance_make_saldo_198_298():
#====================================
# CREATE DEFINER=`test_user`@`localhost` PROCEDURE `balance_make_saldo_198_298`()
# BEGIN
#     drop table if exists saldo_198_298;
#     create temporary table saldo_198_298 as
#
#     select
#        a.dt, a.line, a.lev, a.la_p, a.regn, a.has_iv,
#
#        case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end ir,
#
#        case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end iv,
#
#        case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end
#
#      +    case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end  itogo
#
#     from balance a
#
#     left join balance b
#
#     on a.dt = b.dt and a.regn = b.regn
#
#     where a.line = 198000
#
#     and b.line = 298000
#
#
#     group by a.dt, a.line, a.lev, a.la_p, a.regn
#
#     UNION ALL
#     select
#
#        b.dt, b.line, b.lev, b.la_p, b.regn, b.has_iv,
#
#         case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end ir,
#         case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end iv,
#
#         case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end
#      + case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end itogo
#         from balance a
#     left join balance b
#
#     on a.dt = b.dt and a.regn = b.regn
#
#     where a.line = 198000
#
#     and b.line = 298000
#     group by b.dt, b.line, b.lev, b.la_p, b.regn;
#
#
#     delete from balance where line = 198000;
#
#     delete from balance where line = 298000;
#
#     insert into balance
#
#     select * from saldo_198_298;
# END ;;

#TODO: pandas equivalent of above logic

#balance_make_insert_totals():
#=================================
# CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make_insert_totals`()
# BEGIN
#
#     drop table if exists tmp_balance_total;
#     create table tmp_balance_total as
#     select dt, 100000 line, 1 lev, 1 la_p, regn, has_iv, sum(ir) ir, sum(iv) iv, sum(itogo) itogo from balance
#     where la_p = 1 and line != 100000 and lev = 10
#     group by regn, dt;
#
#     insert into tmp_balance_total
#     select dt, 200000 line, 1 lev, 2 la_p, regn, has_iv, sum(ir) ir, sum(iv) iv, sum(itogo) itogo from balance
#     where la_p = 2 and line != 200000 and lev = 10
#     group by regn, dt;
#
#     drop table if exists balance_net;
#     create temporary table balance_net as
#     select b.dt, 500 line, 1 lev, 0 la_p, b.regn, b.has_iv, (b.ir - z.ir) ir,
#                                                 (b.iv - z.iv) iv,
#                                                               (b.itogo-z.itogo) as itogo
#     from tmp_balance_total b
#     left join tmp_balance_total z on b.dt = z.dt and b.regn = z.regn
#     where b.line = 100000 and z.line = 200000
#     group by dt, regn;
#
#     insert into balance
#     select * from tmp_balance_total;
#
#     insert into balance
#     select * from   balance_net;
#
#     drop table tmp_balance_total;
#     drop table balance_net;
#
# END ;;

#TODO: pandas equivalent of above logic


for var in [f101, alloc, balance]:
    print()
    print(var.head())
    pprint(var.columns.tolist())





