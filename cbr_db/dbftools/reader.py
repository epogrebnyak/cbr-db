from collections import defaultdict
from functools import reduce

from dbfread import DBF


# encoding of the dbf files
CODEPAGE = "cp866"


class CustomDBF(DBF):
    """
    Original DBF reader is quite slow (as for 2.0.4).
    We override `_iter_records` for better reading speed.
    It's about 2 times faster on `11 2015-12-01` dataset.
    """

    def __init__(self, filename, encoding=None, selected_fields=None):
        """
        Custom constructor contains additional argument `selected_fields`.
        It is used to narrow set of fields at the lowest level possible.
        """
        super(CustomDBF, self).__init__(filename, encoding=encoding)
        self.__selected_fields = set(selected_fields)

    def _iter_records(self, record_type=b' '):
        """
        WARNING: we re-use the same dict for yielding.
        It means that caller MUST NOT store yielded results as objects.
        Yielded records must be consumed (to CSV, to DB) and discarded.
        """
        with open(self.filename, 'rb') as infile, self._open_memofile() as memofile:
            # Skip to first record.
            infile.seek(self.header.headerlen, 0)
            field_parser = self.parserclass(self, memofile)
            # We know that our data are mostly numbers, strings and dates,
            # so we can keep local dict for parsing functions.
            parse = defaultdict(lambda x: field_parser.parse)
            parse.update({
                'N': field_parser.parseN,
                'C': field_parser.parseC,
                'D': field_parser.parseD,
            })
            # Shortcuts for speed
            skip_record = self._skip_record
            read = infile.read
            seek = infile.seek
            fields = self.fields
            for field in fields:
                field._sel = (field.name in self.__selected_fields)
            # Squash fields: combine N consecutive unused fields into one.
            # This allows efficient skipping of unused fields by seek().
            fields = self.__squash(fields)
            # Reuse the same dict for speed.
            items = {}
            while True:
                sep = read(1)
                if sep == record_type:
                    for field in fields:
                        if field._sel:
                            items[field.name] = parse[field.type](field, read(field.length))
                        else:
                            seek(field.length, 1)
                    yield items
                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    skip_record(infile)

    @staticmethod
    def __squash(fields):
        """
        Combines N consecutive unused (_sel == False) fields into one fake long field.
        Returns squashed list of fields.
        """
        def squash(fields, field):
            if fields and not fields[-1]._sel and not field._sel:
                fields[-1].length += field.length
            else:
                fields.append(field)
            return fields
        return list(reduce(squash, [[]] + fields))


def get_records(dbf_filename, field_name_selection):
    """
    WARNING: we re-use the same dict for yielding.
    It means that caller MUST NOT store yielded results as objects.
    Yielded records must be consumed (to CSV, to DB) and discarded.
    """
    # Use CustomDBF for speed
    table = CustomDBF(dbf_filename, encoding=CODEPAGE,
                      selected_fields=field_name_selection)
    # Don't iterate and yield, return an iterator directly - it's much faster
    return iter(table.records)
