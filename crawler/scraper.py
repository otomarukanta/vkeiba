from abc import ABCMeta
import aiohttp
import asyncio
import bs4
from crawler.cachedb import CacheDB
from logging import getLogger, config

config.fileConfig('./conf/logging.conf')


class Scraper(metaclass=ABCMeta):

    def __init__(self, parse, store):
        self._baseurl = 'http://keiba.yahoo.co.jp/'
        self._semaphore = asyncio.Semaphore(5)
        self._parse = parse
        self._store = store
        self._cache_db = CacheDB()
        self.logger = getLogger(__name__)

    async def download(self, path):
        self.logger.info('Starting download %s', path)
        res = await aiohttp.request('GET', self._baseurl + path)
        self.logger.info('Finished download %s', path)
        return await res.text()

    async def _fetch_page(self, path):
        if self._cache_db.contains(path):
            self.logger.info('Starting get page from cache in %s', path)
            page = self._cache_db.get(path)
            self.logger.info('Finished get page from cache in %s', path)
        else:
            with (await self._semaphore):
                page = await self.download(path)
            self._cache_db.put(path, page)
        return page

    async def _scrape(self, path):
        page = await self._fetch_page(path)
        soup = bs4.BeautifulSoup(page, 'lxml')
        parsed = self._parse(soup)
        self._store(parsed)

    def crawl(self, paths):
        loop = asyncio.get_event_loop()
        task = [self._scrape(path) for path in paths]
        result = loop.run_until_complete(asyncio.gather(*task))
        return [res for res in result if res]
