from util.offset import Offsets
from util.sizes import Sizes
from util.player_position import PlayerPosition
from util.crypto import decrypt
from parser.base_parser import BaseParser
from entity.player import Player


class PlayersParser(BaseParser):

    def __init__(self, data, players_offs, count_offs):
        self._data = data
        self._players_offs = players_offs
        self._count_offs = count_offs

    def parse(self):
        number_players = self._data[self._count_offs]
        players = []

        for _ in range(0, number_players):
            entry_len = self._data[self._players_offs + Sizes.COUNTRY.value]
            pos_offs = self._players_offs + Sizes.COUNTRY.value + entry_len + 1
            ret = decrypt(self._data, self._players_offs,
                          Sizes.COUNTRY.value + entry_len + 1)

            country = ret[1:4]
            name = ret[5:]
            pos = PlayerPosition.to_pos_name(self._data[pos_offs])

            players.append(Player(name=name, position=pos, country=country))
            # +1 to skip the 'name size' byte
            # +1 to skip the position byte
            # +1 to jump to the next entry
            self._players_offs += Sizes.COUNTRY.value + entry_len + 3

        return players
