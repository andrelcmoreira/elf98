from abc import ABC, abstractmethod


class BaseParser(ABC):

    def get_field(self, data, offset, size):
        return data[offset:offset + size]

    @abstractmethod
    def parse(self):
        pass
