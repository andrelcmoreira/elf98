from serializer.base_serializer import BaseSerializer
from util.crypto import encrypt


class CoachSerializer(BaseSerializer):

    @staticmethod
    def serialize(obj: str) -> bytearray:
        coach = bytearray()

        coach.append(0)
        coach += encrypt(obj)

        return coach
