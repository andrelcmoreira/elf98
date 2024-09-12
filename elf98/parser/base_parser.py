from abc import ABC, abstractmethod


class BaseParser(ABC):

    def get_field(self, data: bytes, offset: int, size: int) -> bytes:
        return data[offset:offset + size]

    @abstractmethod
    def parse(self):
        pass
