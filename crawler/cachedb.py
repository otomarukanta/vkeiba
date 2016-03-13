import os
from datetime import datetime
import dbm


class CacheDB():

    _db_filename = './cache.dbm'

    def __init__(self):
        pass

    def _contains_cache(self, path):
        return os.path.exists(self._hash(path))

    def get(self, path):
        print('Get page from cache in {} at {}'.format(path, datetime.now()))
        with dbm.open(self._db_filename, 'c') as db:
            page = db.get(path)
        return page

    def put(self, path, page):
        with dbm.open(self._db_filename, 'c') as db:
            db[path] = page
