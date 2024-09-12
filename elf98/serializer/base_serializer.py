from abc import abstractstaticmethod, ABC

class BaseSerializer(ABC):

    @abstractstaticmethod
    def serialize(obj: str) -> bytearray:
        pass
