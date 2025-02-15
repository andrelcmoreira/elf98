from json import loads
from re import findall

from entity.player import Player
from provider.base_provider import BaseProvider
from util.player_position import PlayerPosition


class EspnProvider(BaseProvider):

    # Cazaquistão, Curaçao, Eritreia, French Guiana, Gibraltar, Irã, Kosovo,
    # Liechtenstein and Palestina are not mapped by the game
    _COUNTRIES = {
        'África do Sul': 'AFS',
        'Arábia Saudita': 'ASA',
        'Azerbaijão': 'AZB',
        'Bangladesh': 'BGD',
        'Benim': 'BNI',
        'Botsuana': 'BTW',
        'Cape Verde Islands': 'CAV',
        'Catar': 'QAT',
        'Chade': 'CHD',
        'Comoros Islands': 'CMR',
        'Congo (Brazavile)': 'CNG',
        'Costa do Marfim': 'CMF',
        'Costa Rica': 'CRC',
        'Chile': 'CHL',
        'China': 'CHN',
        'China PR': 'CHN',
        'Chipre': 'CHP',
        'Czechia': 'RCH',
        'Coreia do Sul': 'CRS',
        'Egito': 'EGT',
        'Eslováquia': 'EVQ',
        'Eslovênia': 'EVN',
        'Gana': 'GNA',
        'Gâmbia': 'GMB',
        'Granada': 'GRN',
        'Haiti': 'HTI',
        'Mauritânia': 'MRT',
        'Namíbia': 'NMI',
        'Nova Zelândia': 'NZE',
        'País de Gales': 'WAL',
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

    def assemble_uri(self, team_id: str, season: str) -> str:
        return f'{self._base_url}{team_id}/season/{season}' if season else \
            self._base_url + team_id

    def parse_reply(self, reply: str) -> list | None:
        ret = findall(r'(\"athletes\":[\'\[\{"\w:,\/\.\d~\-\s\}\\p{L}\(\)]+\])',
                      reply.text)

        try:
            goalkeepers = loads('{' + ret[0] + '}')
            others = loads('{' + ret[1] + '}')

            return self._parse_players(goalkeepers['athletes'] + \
                                       others['athletes'])
        except IndexError:
            return None

    def select_players(self, player_list: list) -> list:
        players = []
        gk = []
        df = []
        mf = []
        fw = []

        for player in player_list:
            match player.position:
                case PlayerPosition.G.name: gk.append(player)
                case PlayerPosition.D.name: df.append(player)
                case PlayerPosition.M.name: mf.append(player)
                case PlayerPosition.A.name: fw.append(player)

        gk.sort(key=lambda p: int(p.appearances), reverse=True)
        df.sort(key=lambda p: int(p.appearances), reverse=True)
        mf.sort(key=lambda p: int(p.appearances), reverse=True)
        fw.sort(key=lambda p: int(p.appearances), reverse=True)

        # TODO: check the maximum number of players allowed by the game
        players.extend(gk[0:self._MAX_GK_PLAYERS])
        players.extend(df[0:self._MAX_DEF_PLAYERS])
        players.extend(mf[0:self._MAX_MD_PLAYERS])
        players.extend(fw[0:self._MAX_FW_PLAYERS])

        return players

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
