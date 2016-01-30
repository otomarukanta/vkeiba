from abc import ABCMeta, abstractmethod
import os


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
