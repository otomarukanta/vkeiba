from abc import ABCMeta, abstractmethod
import aiohttp
import asyncio
import bs4
from datetime import datetime


class Scraper(metaclass=ABCMeta):

    def __init__(self):
        self._baseurl = 'http://keiba.yahoo.co.jp/'
        self._semaphore = asyncio.Semaphore(5)

    @abstractmethod
    def _parse():
        pass

    async def download(self, path):
        print('starting download {} at {}'.format(path, datetime.now()))
        res = await aiohttp.request('GET', self._baseurl + path)
        print('finished download {} at {}'.format(path, datetime.now()))
        return await res.text()

    async def _scrape(self, path):
        with (await self._semaphore):
            page = await self.download(path)
        self.soup = bs4.BeautifulSoup(page, 'lxml')
        return self._parse()

    def crawl(self, paths):
        loop = asyncio.get_event_loop()
        task = [self._scrape(path) for path in paths]
        result = loop.run_until_complete(asyncio.gather(*task))
        return result
