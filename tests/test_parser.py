import os
import json
import bs4
from unittest import TestCase
from nose.tools import eq_
from crawler import parser
from crawler import race_parser

resources_dir = '{}/resources/'.format(os.path.dirname(__file__))


class TestParser(TestCase):
    def test_schedule_list(self):
        expected = ['/path/to/foo1/', '/path/to/foo2/', '/path/to/foo3/']
        with open('{}schedule_list.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_schedule_list(soup)
        eq_(expected, actual)

    def test_race_list(self):
        expected = ['/path/to/bar1/', '/path/to/bar2/', '/path/to/bar3/']
        with open('{}race_list.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_race_list(soup)
        eq_(expected, actual)

    def test_race_result(self):
        from tests.resources import race_result
        with open('{}race_result.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = race_parser.RaceResultParser().parse(soup)
        expected = race_result.expected
        try:
            eq_(actual, expected)
        except AssertionError:
            for k, v in expected.items():
                self.assertEqual(actual[k], v)

    def test_horse(self):
        from tests.resources import horse
        with open('{}horse.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_horse(soup)
        eq_(horse.expected, actual)

    def test_jockey(self):
        with open('{}/jockey.json'.format(resources_dir)) as f:
            expected = json.load(f)
        with open('{}jockey.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_jockey(soup)
        eq_(expected, actual)

    def test_trainer(self):
        with open('{}/trainer.json'.format(resources_dir)) as f:
            expected = json.load(f)
        with open('{}trainer.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_trainer(soup)
        eq_(expected, actual)
