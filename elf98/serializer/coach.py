from serializer.base_serializer import BaseSerializer
from util.player_position import PlayerPosition
from util.crypto import encrypt


class CoachSerializer(BaseSerializer):

    def serialize(obj):
        coach = bytearray()

        coach.append(0)
        coach += encrypt(obj)

        return coach
