from abc import ABCMeta, abstractmethod
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crawler import model


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


class RaceResultStorage(Storage):

    def __init__(self, jockey_filename, horse_filename, trainer_filename):
        self._jockey_storage = PathStorage(jockey_filename)
        self._horse_storage = PathStorage(horse_filename)
        self._trainer_storage = PathStorage(trainer_filename)
        with open('conf/db.json', 'r') as f:
            string = 'postgresql+psycopg2://{user}:{passwd}@{host}/{db}'
            engine = create_engine(string.format(**json.load(f)))

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def store(self, data):
        self._jockey_storage.store(data['jockey'])
        self._horse_storage.store(data['horse'])
        self._trainer_storage.store(data['trainer'])

        for record in data['result']:
            self.session.add(model.RaceResult(**record))

        self.session.add(model.RaceInfo(**data['info']))
        self.session.commit()
