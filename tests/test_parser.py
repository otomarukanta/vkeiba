import os
import json
import bs4
from unittest import TestCase
from nose.tools import eq_
from crawler import parser

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
        with open('{}/race_result.json'.format(resources_dir)) as f:
            expected = json.load(f)
        with open('{}race_result.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_race_result(soup)
        eq_(expected, actual)

    def test_horse(self):
        with open('{}/horse.json'.format(resources_dir)) as f:
            expected = json.load(f)
        with open('{}horse.html'.format(resources_dir), 'r') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        actual = parser.parse_horse(soup)
        eq_(expected, actual)

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
