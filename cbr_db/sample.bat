call baf reset database raw
call baf reset database final    
call baf download     101 2015-01-01
call baf unpack       101 2015-01-01
call baf make csv     101 2015-01-01
call baf import csv   101 2015-01-01
call baf make dataset 101 2015-01-01 
call baf migrate dataset 101        
call baf make balance
call baf report balance --xls