import os
from unittest import TestCase
from nose.tools import eq_, ok_
from crawler.storage import PathStorage

resources_dir = '{}/resources/'.format(os.path.dirname(__file__))


class TestPathStorage(TestCase):

    filename = '/tmp/test_path_storage.txt'

    def setUp(self):
        self.storage = PathStorage(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_file_exists(self):
        filename = '/tmp/path_storage.txt'
        PathStorage(filename)
        ok_(os.path.isfile(filename))
        os.remove('/tmp/path_storage.txt')

    def test_duplicate_path(self):
        self.storage.store(['/path/aaa/'])
        self.storage.store(['/path/aaa/'])
        with open(self.filename) as f:
            actual = f.read()
        expect = '/path/aaa/\n'
        eq_(actual, expect)
