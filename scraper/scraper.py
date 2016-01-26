from abc import ABCMeta, abstractmethod
import aiohttp
import asyncio
import bs4
from datetime import datetime
import os
import hashlib
import gzip


class Scraper(metaclass=ABCMeta):

    def __init__(self):
        self._baseurl = 'http://keiba.yahoo.co.jp/'
        self._semaphore = asyncio.Semaphore(5)

    @abstractmethod
    def _parse():
        pass

    def _hash(self, path):
        return 'cache/{}'.format(hashlib.md5(path.encode('utf-8')).hexdigest())

    def _contains_cache(self, path):
        return os.path.exists(self._hash(path))

    def _get_cache(self, path):
        print('Get page from cache in {} at {}'.format(path, datetime.now()))
        with gzip.open(self._hash(path), 'rb') as f:
            data = f.read()
        return data

    def _save_cache(self, path, page):
        if not os.path.isdir('cache'):
            os.mkdir('cache')
        with gzip.open(self._hash(path), 'wb') as f:
            f.write(page.encode('utf-8'))

    async def download(self, path):
        print('starting download {} at {}'.format(path, datetime.now()))
        res = await aiohttp.request('GET', self._baseurl + path)
        print('finished download {} at {}'.format(path, datetime.now()))
        return await res.text()

    async def _scrape(self, path):
        if self._contains_cache(path):
            page = self._get_cache(path)
        else:
            with (await self._semaphore):
                page = await self.download(path)
            self._save_cache(path, page)
        self.soup = bs4.BeautifulSoup(page, 'lxml')
        return self._parse()

    def crawl(self, paths):
        loop = asyncio.get_event_loop()
        task = [self._scrape(path) for path in paths]
        result = loop.run_until_complete(asyncio.gather(*task))
        return [res for res in result if res]
