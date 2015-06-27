import os
import csv
from datetime import datetime
from global_ini import DIRLIST, FORM_DATA
from dbfread import DBF
from date_engine import isodate2timestamp, iso2date, date2quarter, date2iso

CODEPAGE = "cp866"

def get_records(dbf_filename, field_name_selection):
    table = DBF(dbf_filename, encoding=CODEPAGE)

    for record in table.records:
        result = {key: value for key, value in record.items() if key in field_name_selection}
        yield result

def make_csv_filename(dbf_filename, db_table_name):
    if db_table_name is None:
        #  rename if db_table_name not supplied
        csv_filename = dbf_filename[:-4] + ".csv"
    else:
        # make dbf filename same as table name, put date information in extension
        csv_filename = db_table_name + "." + dbf_filename[:-4]

    return csv_filename

def make_dbf_filename(isodate, postfix, form):
    ts = isodate2timestamp(form, isodate)
    dbf_filename = ts + postfix + ".DBF"
    return dbf_filename

def write_csv_by_path(dbf_path, csv_path, field_name_selection, form, dt):
    # not todo - make time wrapper
    startTime = datetime.now()
    # ----------------------
    with open(csv_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter='\t', lineterminator='\n',  fieldnames=field_name_selection)
        writer.writeheader()
        
        n_skipped = 0

        for rec_dict in get_records(dbf_path, field_name_selection):
            skip = False
            
            if form == "101":
                if "NUM_SC" in field_name_selection and rec_dict["NUM_SC"] != "ITGAP":
                    for c in ("IITG", "ITOGO"):
                        if c in field_name_selection:
                            rec_dict[c] = int(rec_dict[c])
                else:
                    skip = True
            
            if form == "102":
                # fix (fill with zeros) SIM_R and SIM_V
                for c in ("SIM_R", "SIM_V"):
                    if c in field_name_selection and rec_dict[c] is None:
                        rec_dict[c] = 0
                
                # add date, year and quarter
                rec_dict["DT"] = date2iso(dt)
                
                qt_year, qt_month = date2quarter(dt)                
                rec_dict["YEAR"] = qt_year
                rec_dict["QUART"] = qt_month
                    
            if skip:
                n_skipped += 1
            else:
                writer.writerow(rec_dict)
    # ----------------------
    msg = "Time elapsed: {0}".format(datetime.now() - startTime)

    if n_skipped > 0:
        msg = msg + "\nSkipped writing {0} records to file.".format(n_skipped)

    print(msg)

def write_csv(dbf_filename, field_name_selection, db_table_name, dbf_dir, csv_dir, form,
              dt):
    csv_filename = make_csv_filename(dbf_filename, db_table_name)
    csv_path = os.path.join(csv_dir, csv_filename)
    dbf_path = os.path.join(dbf_dir, dbf_filename)

    if os.path.isfile(dbf_path):
        print("Converting {0} to csv file {1}".format(dbf_filename, csv_filename))
        write_csv_by_path(dbf_path, csv_path, field_name_selection, form, dt)
    else:
        print("File {0} not found".format(dbf_filename))

def dbf2csv(isodate, form):
    """
    Converts DBF files to CSV files with SQL table name as basename and date as extension.
    This filename format allows using fast mysqlimport to read CSV files to database.
    Function will iterate over subforms in each form.
    """
    for subform, info in FORM_DATA[form].items():
        write_csv(dbf_filename=make_dbf_filename(isodate, info['postfix'], form),
                  field_name_selection=info['dbf_fields'],
                  db_table_name=info['db_table'],
                  dbf_dir=DIRLIST[form]['dbf'],
                  csv_dir=DIRLIST[form]['csv'],
                  form=form,
                  dt=iso2date(isodate))

def list_csv_filepaths_by_date(isodate, form):
    for subform, info in FORM_DATA[form].items():
        dbf_filename = make_dbf_filename(isodate, info['postfix'], form)
        csv_filename = make_csv_filename(dbf_filename, info['db_table'])
        csv_dir = DIRLIST[form]['csv']
        csv_path = os.path.join(csv_dir, csv_filename)
        yield csv_path

if __name__ == "__main__":
    form_n = "101"
    #
    print(DIRLIST[form_n])

    # Access to FORM_DATA - example 1
    for sub in ['f101_B', 'f101_B']:
        z = FORM_DATA[form_n][sub]
        print(z)

    # Access to FORM_DATA - example 2
    for key, val in FORM_DATA[form_n].items():
        print(val['name'])
