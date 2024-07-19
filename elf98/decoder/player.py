from data.offsets import Offsets
from data.sizes import Sizes
from data.player_position import PlayerPosition
from decoder.base import BaseParser
from entity.player import Player


class PlayersParser(BaseParser):

    def __init__(self, data, players_offs, count_offs):
        self._data = data
        self._players_offs = players_offs
        self._count_offs = count_offs

    def _get_player_pos(self, pos_code):
        pos = ''

        match pos_code:
            case PlayerPosition.G.value: pos = PlayerPosition.G.name
            case PlayerPosition.D.value: pos = PlayerPosition.D.name
            case PlayerPosition.M.value: pos = PlayerPosition.M.name
            case PlayerPosition.A.value: pos = PlayerPosition.A.name

        return pos

    def parse(self):
        number_players = self._data[self._count_offs]
        players = []

        for _ in range(0, number_players):
            entry_len = self._data[self._players_offs + Sizes.COUNTRY.value]
            pos_offs = self._players_offs + Sizes.COUNTRY.value + entry_len + 1
            ret = self.decrypt_field(self._data, self._players_offs,
                                     Sizes.COUNTRY.value + entry_len + 1)

            country = ret[1:4]
            name = ret[5:]
            pos = self._get_player_pos(self._data[pos_offs])

            players.append(Player(name=name, position=pos, country=country))
            # +1 to skip the 'name size' byte
            # +1 to skip the position byte
            # +1 to jump to the next entry
            self._players_offs += Sizes.COUNTRY.value + entry_len + 3

        return players
