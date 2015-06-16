# -*- coding: utf-8 -*-
# todo: add this header to other files
import csv
import datetime
import re
import os
import sys
from global_ini import get_private_data_folder

# Risk: hardcoded 101
FORM_DIR = get_private_data_folder('101', 'txt')
CSV_DIR  = get_private_data_folder('101', 'csv')
SUBDIR   = [2011, 2012, 2013, 2014, 2015]
DB_VEB_TABLE = "bulk_f101veb"

def convert_txt_directory_to_csv(private_data_folder = FORM_DIR):
    for year in SUBDIR:
        directory = os.path.join(private_data_folder, str(year))
        for filename in os.listdir(directory):
            if is_vaild_filename(filename):
                print("Converting <" + filename + "> from <" + directory + ">")
                txt2csv(filename, year, sourcedir=directory)

# todo: this function is a duplicate, it is contained in other module. need to import instaed 
def shift_month_ahead(date):
     if date.month < 12:
         date = date.replace(month = date.month + 1)
     else:
         date = date.replace(month = 1)
         date = date.replace(year = date.year + 1)
     return(date)

def is_vaild_filename(filename):
    fn, d = get_target_file_name_and_date(filename, 1)
    if fn is not None: 
        return True
    else: 
        return False

def get_target_file_name_and_date(sourcefile, year, target_directory = CSV_DIR):
    regex = r"(?i)^F101_([0-9]{2}).TXT$" 
    sre   = re.match (regex, sourcefile)
    if sre is not None:
        month = int(sre.group(1))
        date  = shift_month_ahead(datetime.date(year,month,1))
        isodate = date.strftime("%Y-%m-%d")
        csv_file = os.path.join(target_directory, DB_VEB_TABLE + "." + isodate)
        return (csv_file, isodate)
    else:
        return (None, None)

def txt2csv (sourcefile, year, sourcedir=None):       
    csv_file, isodate = get_target_file_name_and_date(sourcefile, year)
    with open(csv_file, 'w') as targetfile:
        spamwriter = csv.writer(targetfile, delimiter='\t', lineterminator = '\n')
        sourcefile = os.path.join(sourcedir,sourcefile)
        with open(sourcefile, 'r') as sourcefile:
            spamreader = csv.reader(sourcefile, delimiter=' ', skipinitialspace = True)
            is_in_section_a = False
            is_in_section_b = False
            a_p = 0
            
            for row in spamreader:
                if len(row) > 0:
                    if is_in_section_a == False and row[0] == u"А.": is_in_section_a = True
                    if is_in_section_b == False and row[0] == u"Б.": is_in_section_b = True
                    if is_in_section_a == True and row[0] == u"Актив": a_p = 1
                    if is_in_section_a == True and row[0] == u"Пассив": a_p = 2
                    if is_in_section_b == True: a_p = 0
                    #  print(a_p)
                    
                if len(row) > 0:  flag = (
                                  "|" == row[0][0] 
                              and len(row[0]) > 1
                              and len(row)  == 13
                              )
                if flag:
                    row[0] = row[0][1:]
                    row[-1] = row[-1][:-1]
                    row.append(isodate)
                    row.append(str(a_p))
                    #print (', '.join(row))
                    spamwriter.writerow(row)              
