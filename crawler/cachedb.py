import dbm
import codecs


class CacheDB():

    _db_filename = './cache.dbm'
    _comp_format = 'bz2'

    def __init__(self):
        pass

    def contains(self, path):
        with dbm.open(self._db_filename, 'c') as db:
            return path in db

    def get(self, path):
        with dbm.open(self._db_filename, 'c') as db:
            page = db.get(path)
        if page is None:
            return None
        return codecs.decode(page, self._comp_format).decode()

    def put(self, path, page):
        with dbm.open(self._db_filename, 'c') as db:
            db[path] = codecs.encode(page.encode(), self._comp_format)
