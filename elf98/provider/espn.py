from json import loads
from re import findall
from requests import get

from entity.player import Player
from provider.base_provider import BaseProvider
from util.country import get_country


class EspnProvider(BaseProvider):

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

            return self._parse_players(goalkeepers, others)
        except IndexError:
            return None

    def _parse_players(self, goalkeepers, others):
        players = []

        for player in goalkeepers['athletes']:
            if not player['ctz']: # ignore players with unknown country
                continue

            players.append(
                Player(
                    name=player['name'],
                    position=player['position'],
                    country=get_country(player['ctz']),
                    appearances=player.get('appearances') \
                        if player.get('appearances') is not None \
                        else 0
                )
            )

        for player in others['athletes']:
            if not player['ctz']: # ignore players with unknown country
                continue

            players.append(
                Player(
                    name=player['name'],
                    position=player['position'],
                    country=get_country(player['ctz']),
                    appearances=player.get('appearances') \
                        if player.get('appearances') is not None \
                        else 0
                )
            )

        return players
