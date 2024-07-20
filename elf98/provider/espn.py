from provider.base import Base
from entity.player import Player
from util.country import get_country

from json import load, loads
from re import findall
from requests import get


class EspnProvider(Base):

    def parse_mapping(self):
        pass

    def get_team_id(self, equipa_file):
        with open('data/espn.json') as f:
            mapping = load(f)

            for entry in mapping:
                if entry['file'] == equipa_file:
                    return entry['id']

            return ''

    def fetch_team_data(self, team_id):
        base_url = 'https://www.espn.com.br/futebol/time/elenco/_/id/'
        headers = { 'User-Agent': 'elf98' }
        reply = get(base_url + team_id, headers=headers, timeout=5)

        ret = findall(r'(\"athletes\":[\[\{"\w:,\/\.\d~\-\s\}\\p{L}]+\])',
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

        return self.select_players(players)
