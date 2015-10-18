#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import chain
from scraper.schedule_list_scraper import ScheduleListScraper
from scraper.race_list_scraper import RaceListScraper
from scraper.race_result_scraper import RaceResultScraper


class YahooKeibaSpider():
    def __init__(self):
        self.schedule_list_scraper = ScheduleListScraper()
        self.race_list_scraper = RaceListScraper()
        self.race_result_scraper = RaceResultScraper()

    def crawl(self, date):
        # fetch race/list/ paths
        paths = ["schedule/list/{}/?month={}".format(year, month)
                 for year, month in date]
        race_list_paths = self.schedule_list_scraper.crawl(paths)

        # fetch race/result/ paths
        race_list_paths = list(chain.from_iterable(race_list_paths))
        race_result_paths = self.race_list_scraper.crawl(race_list_paths)

        # get race info, race result, jockey path, horse path, trainer path
        race_result_paths = list(chain.from_iterable(race_result_paths))
        result_dicts = self.race_result_scraper.crawl(race_result_paths)

        print(result_dicts)

if __name__ == "__main__":
    spider = YahooKeibaSpider()
    spider.crawl([(2015, 11)])
