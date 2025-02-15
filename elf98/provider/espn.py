from json import loads
from re import findall
from requests import get

from entity.player import Player
from provider.base_provider import BaseProvider


class EspnProvider(BaseProvider):

    _MAX_NAME_SIZE = 18
    _COUNTRIES = {
        'África do Sul': 'AFS',
        'Arábia Saudita': 'ASA',
        'Azerbaijão': 'AZB',
        'Bangladesh': 'BGD',
        'Benim': 'BNI',
        'Botsuana': 'BTW',
        'Cape Verde Islands': 'CAV',
        'Catar': 'QAT',
        #'Cazaquistão': '',
        'Chade': 'CHD',
        'Comoros Islands': 'CMR',
        'Congo (Brazavile)': 'CNG',
        'Costa do Marfim': 'CMF',
        'Costa Rica': 'CRC',
        'Chile': 'CHL',
        'China': 'CHN',
        'China PR': 'CHN',
        'Chipre': 'CHP',
        #'Curaçao': '',
        'Czechia': 'RCH',
        'Coreia do Sul': 'CRS',
        'Egito': 'EGT',
        #'Eritreia': '',
        'Eslováquia': 'EVQ',
        'Eslovênia': 'EVN',
        #'French Guiana': '',
        'Gana': 'GNA',
        'Gâmbia': 'GMB',
        #'Gibraltar': '',
        'Granada': 'GRN',
        #'Irã': '',
        #'Kosovo': '',
        #'Liechtenstein': '',
        'Haiti': 'HTI',
        'Mauritânia': 'MRT',
        'Namíbia': 'NMI',
        'Nova Zelândia': 'NZE',
        'País de Gales': 'WAL',
        #'Palestina': '',
        'Trinidad e Tobago': 'TND',
        'USA': 'EUA',
        'Venezuela': 'VNZ',
        'Republic of Ireland': 'IRL',
        'República da Sérvia': 'SER',
        'República Democrática do Congo': 'CNG',
        'República Centro-Africana': 'RCA',
        'República Dominicana': 'RDO',
        'Zimbábue': 'ZBW'
    }

    def __init__(self):
        super().__init__('espn',
                         'https://www.espn.com.br/futebol/time/elenco/_/id/',
                         self._COUNTRIES)

    def fetch_team_data(self, team_id: str, season: str) -> list | None:
        uri = self._base_url + team_id + f'/season/{season}' if season else \
            self._base_url + team_id
        headers = { 'User-Agent': 'elf98' }

        # TODO: handle timeout
        reply = get(uri, headers=headers, timeout=5)

        ret = findall(r'(\"athletes\":[\'\[\{"\w:,\/\.\d~\-\s\}\\p{L}\(\)]+\])',
                      reply.text)

        try:
            goalkeepers = loads('{' + ret[0] + '}')
            others = loads('{' + ret[1] + '}')

            return self._parse_players(goalkeepers['athletes'] + \
                                       others['athletes'])
        except IndexError:
            return None

    def _get_player_name(self, player: dict) -> str:
        return player['name'] \
            if len(player['name']) <= self._MAX_NAME_SIZE \
            else player['shortName']

    def _parse_players(self, data: list) -> list:
        players = []

        for player in data:
            if not player['ctz']: # ignore players with unknown country
                continue

            players.append(
                Player(
                    name=self._get_player_name(player),
                    position=player['position'],
                    country=self.get_country(player['ctz']),
                    appearances=player.get('appearances', 0)
                )
            )

        return players
