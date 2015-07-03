import csv
import datetime
import re
import os
from global_ini import get_private_data_folder
from date_engine import shift_month_ahead, date2iso, quarter2date

FORM_DIR = get_private_data_folder('txt')
CSV_DIR = get_private_data_folder('csv')
YEARS = [2013]

def convert_txt_directory_to_csv(private_data_folder=FORM_DIR):
    """
    Converts all supported text files from <private_data_folder> to csv files.
    """
    for year in YEARS:
        directory = os.path.join(private_data_folder, str(year))
        
        for filename in os.listdir(directory):
            converter = get_converter_for_file(filename)
            
            if converter:
                path = os.path.join(directory, filename)
                print("Converting {} to csv".format(path))
                converter(path, year)
            else:
                print("Skipping {}: no suitable converter found".format(filename))
                
def f101_txt2csv(filename, year):
    """
    Special converter of form 101 text files to csv files.
    """
    month = int(os.path.basename(filename)[5:7])
    isodate = date2iso(shift_month_ahead(datetime.date(year, month, 1)))
    csv_file = os.path.join(CSV_DIR, "bulk_f101veb.{}".format(isodate))
    
    with open(csv_file, 'w') as targetfile:
        writer = csv.writer(targetfile, delimiter='\t', lineterminator = '\n')

        with open(filename, 'r') as sourcefile:
            reader = csv.reader(sourcefile, delimiter=' ', skipinitialspace = True)
            is_in_section_a = False
            is_in_section_b = False
            a_p = 0
            
            for row in reader:
                if len(row) > 0:
                    if is_in_section_a == False and row[0] == u"А.": is_in_section_a = True
                    if is_in_section_b == False and row[0] == u"Б.": is_in_section_b = True
                    if is_in_section_a == True and row[0] == u"Актив": a_p = 1
                    if is_in_section_a == True and row[0] == u"Пассив": a_p = 2
                    if is_in_section_b == True: a_p = 0
                    #  print(a_p)
                    
                if len(row) > 0:
                    flag = "|" == row[0][0] and len(row[0]) > 1 and len(row) == 13
                    
                if flag:
                    row[0] = row[0][1:]
                    row[-1] = row[-1][:-1]
                    row.append(isodate)
                    row.append(str(a_p))
                    writer.writerow(row)
                    
def f102_txt2csv(filename, year):
    """
    Special converter of form 102 text files to csv files.
    Note: skips rows with missing ('X') values.
    """
    SKIP_ROWS = 45
    quarter = int(os.path.basename(filename)[5])
    isodate = date2iso(quarter2date(year, quarter))
    csv_file = os.path.join(CSV_DIR, "bulk_f102veb.{}".format(isodate))
    
    with open(csv_file, 'w') as targetfile:
        writer = csv.writer(targetfile, delimiter='\t', lineterminator = '\n')

        with open(filename, 'r') as sourcefile:
            reader = csv.reader(sourcefile, delimiter='|', skipinitialspace=True)

            for _ in range(SKIP_ROWS):
                next(reader)
            
            for row in reader:
                if len(row) == 8:
                    try:
                        _ = int(row[1]) # just try to parse, should be int
                        fields = list(map(int, row[3:7]))
                        fields.insert(0, isodate)
                        writer.writerow(fields)
                    except ValueError:
                        pass                        
                
# relates the filename pattern to a special converter
PATTERNS = [
    (r"(?i)^F101_([0-9]{2}).txt$", f101_txt2csv),
    (r"(?i)^F102_([1-4]{1}).txt$", f102_txt2csv)
]
                
def get_converter_for_file(filename):
    """
    Returns a suitable converter (if exists) for the file pointer by <filename>.
    """
    for pattern, converter in PATTERNS:
        sre = re.match(pattern, filename)
        
        if sre:
            return converter
            
if __name__ == "__main__":
    convert_txt_directory_to_csv()