from datetime import datetime
import csv

from cbr_db.utils.dates import date2iso
from cbr_db.utils.dates import date2quarter


def write_csv_by_path(dbf_records, csv_path, field_name_selection, form, dt):
    # not todo - make time wrapper
    startTime = datetime.now()
    # ----------------------
    with open(csv_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                delimiter='\t', lineterminator='\n',
                                fieldnames=field_name_selection)
        writer.writeheader()

        n_skipped = 0

        for rec_dict in dbf_records:
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

    # not todo: may also write skipped rows to separate file
    if n_skipped > 0:
        msg = msg + "\nSkipped writing {0} records to file.".format(n_skipped)

    print(msg)
