from json import loads
from re import findall
from requests import get

from entity.player import Player
from provider.base_provider import BaseProvider
from util.country import get_country


class EspnProvider(BaseProvider):

    MAX_NAME_SIZE = 18

    def __init__(self):
        super().__init__('espn',
                         'https://www.espn.com.br/futebol/time/elenco/_/id/')

    def fetch_team_data(self, team_id):
        headers = { 'User-Agent': 'elf98' }
        reply = get(self._base_url + team_id,
                    headers=headers,
                    timeout=5)

        ret = findall(r'(\"athletes\":[\'\[\{"\w:,\/\.\d~\-\s\}\\p{L}\(\)]+\])',
                      reply.text)

        try:
            goalkeepers = loads('{' + ret[0] + '}')
            others = loads('{' + ret[1] + '}')

            return self._parse_players(goalkeepers['athletes'] + \
                                       others['athletes'])
        except IndexError:
            return None

    def _get_player_name(self, player):
        return player['name'] \
            if len(player['name']) <= self.MAX_NAME_SIZE \
            else player['shortName']

    def _get_player_appearances(self, player):
        return player.get('appearances') \
            if player.get('appearances') is not None \
            else 0

    def _parse_players(self, data):
        players = []

        for player in data:
            if not player['ctz']: # ignore players with unknown country
                continue

            players.append(
                Player(
                    name=self._get_player_name(player),
                    position=player['position'],
                    country=get_country(player['ctz']),
                    appearances=self._get_player_appearances(player)                )
            )

        return players
