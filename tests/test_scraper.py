import os
import json
from unittest import mock, TestCase
from nose.tools import eq_
from scraper.schedule_list_scraper import ScheduleListScraper
from scraper.race_list_scraper import RaceListScraper
from scraper.race_result_scraper import RaceResultScraper

resources_dir = '{}/resources/'.format(os.path.dirname(__file__))

async def download(path):
    with open('{}/{}'.format(resources_dir, path)) as f:
        data = f.read()
    return data


class TestScraper(TestCase):
    def test_schedule_list(self):
        scraper = ScheduleListScraper()
        scraper.download = mock.MagicMock(side_effect=download)
        expected = [['/path/to/foo1/', '/path/to/foo2/', '/path/to/foo3/']]
        actual = scraper.crawl(['schedule_list.html'])
        eq_(expected, actual)

    def test_race_list(self):
        scraper = RaceListScraper()
        scraper.download = mock.MagicMock(side_effect=download)
        expected = [['/path/to/bar1/', '/path/to/bar2/', '/path/to/bar3/']]
        actual = scraper.crawl(['race_list.html'])
        eq_(expected, actual)

    def test_race_result(self):
        scraper = RaceResultScraper()
        scraper.download = mock.MagicMock(side_effect=download)
        with open('{}/race_result.json'.format(resources_dir)) as f:
            expected = [json.load(f)]
        actual = scraper.crawl(['race_result.html'])
        eq_(expected, actual)
