import os

from cbr_db.conf import settings
from cbr_db.database.process import mysqldump

from .common import read_tail


def test_mysqldump(mocker, tempdir):
    db_name = settings.DB_NAME_FINAL
    file_path = os.path.join(tempdir, db_name + '.sql')
    mocker.patch('cbr_db.database.process.get_db_dumpfile_path', return_value=file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
    mysqldump(db_name)
    assert 'Dump completed' in read_tail(file_path, 1024)
