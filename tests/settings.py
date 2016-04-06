import tempfile

from settings import *  # NOQA


DB_SQLITE = os.path.join(tempfile.gettempdir(), 'cbr-db-tests', 'db.sqlite')
