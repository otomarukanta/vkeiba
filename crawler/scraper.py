from abc import ABCMeta
import aiohttp
import asyncio
import bs4
from datetime import datetime
from crawler.cachedb import CacheDB


class Scraper(metaclass=ABCMeta):

    def __init__(self, parse, store):
        self._baseurl = 'http://keiba.yahoo.co.jp/'
        self._semaphore = asyncio.Semaphore(5)
        self._parse = parse
        self._store = store
        self._cache_db = CacheDB()

    async def download(self, path):
        print('starting download {} at {}'.format(path, datetime.now()))
        res = await aiohttp.request('GET', self._baseurl + path)
        print('finished download {} at {}'.format(path, datetime.now()))
        return await res.text()

    async def _scrape(self, path):
        page = self._cache_db.get(path)
        if page is None:
            with (await self._semaphore):
                page = await self.download(path)
            self._cache_db.put(path, page)
        soup = bs4.BeautifulSoup(page, 'lxml')
        parsed = self._parse(soup)
        self._store(parsed)

    def crawl(self, paths):
        loop = asyncio.get_event_loop()
        task = [self._scrape(path) for path in paths]
        result = loop.run_until_complete(asyncio.gather(*task))
        return [res for res in result if res]
