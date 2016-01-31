from abc import ABCMeta, abstractmethod
import os
import json
import pymysql


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def store(self, data):
        pass


class PathStorage(Storage):

    def __init__(self, filename):
        self._filename = filename
        if not os.path.isfile(filename):
            open(self._filename, 'a').close()

    def store(self, data):
        with open(self._filename, 'r') as f:
            wrote_paths = f.read().split('\n')
        paths = [path for path in data if path not in wrote_paths]

        if paths:
            with open(self._filename, 'a') as f:
                f.write('\n'.join(paths))
                f.write('\n')


class MySQL():

    def __init__(self):
        with open('conf/db.json', 'r') as f:
            self._cursor = pymysql.connect(**json.load(f)).cursor()

    def manyinsert(self, table, dic_list):
        for dic in dic_list:
            self.insert(table, dic)

    def insert(self, table, dic):
        values = ["'{}'".format(v) for v in dic.values()]
        statement = 'INSERT INTO {} ({}) VALUES ({})'.format(
                    table, ','.join(dic.keys()), ','.join(values))
        print(statement)
        self._cursor.execute(statement)


class RaceResultStorage(Storage):

    def __init__(self, jockey_filename, horse_filename, trainer_filename):
        self._jockey_storage = PathStorage(jockey_filename)
        self._horse_storage = PathStorage(horse_filename)
        self._trainer_storage = PathStorage(trainer_filename)
        self._mysql = MySQL()

    def store(self, data):
        self._jockey_storage.store(data['jockey'])
        self._horse_storage.store(data['horse'])
        self._trainer_storage.store(data['trainer'])

        self._mysql.manyinsert('race_result', data['result'])
        self._mysql.insert('race_info', data['info'])
