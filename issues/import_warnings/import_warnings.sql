# 12:22 17.06.2015

# Replicating
#
# mysqlimport --ignore_lines=1 --ignore dbf_db3 "D:\databases\ep_bf-master\ep_bf-master\data.downloadable\101\csv.full\bulk_f101b1.122014B1"
#
# as called by 
#
# python bankform.py import csv 101 2015-01-01
#
# Documentation: http://dev.mysql.com/doc/refman/5.1/en/load-data.html
#
#

delete from bulk_f101b1 where dt = "2015-01-01";
LOAD DATA INFILE "D:\\databases\\ep_bf-master\\ep_bf-master\\data.downloadable\\101\\csv.full\\bulk_f101b1.122014B1"
    IGNORE
    INTO TABLE bulk_f101b1
    IGNORE 1 LINES;

# show errors;
# show warnings;
# select * from bulk_f101b1 where dt = "2015-01-01"

/*
problem: even if I delete the date entries from the database I still get a warning in mysqlimport.

dbf_db3.bulk_f101b1: Records: 19163  Deleted: 0  Skipped: 19163  Warnings: 19163
Elapsed time: 0.92

I cannot replicate this behaviour in 'LOAD DATA INFILE' statement and see all the warnings.

This should be some other error, not the duplicate keys, I suppose. You can also try reset entire database
and try import, see if there will be warnings in mysqlimport or LOAD DATA INFILE.

*/






