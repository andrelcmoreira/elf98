from json import loads
from re import findall

from entity.player import Player
from provider.base_provider import BaseProvider
from util.player_position import PlayerPosition


class EspnProvider(BaseProvider):

    # Cazaquistão, Curaçao, Eritreia, El salvador, French Guiana, Gibraltar,
    # Irã, Kosovo, Neocaledonia, Liechtenstein, Palestina and Saint Martin are
    # not mapped by the game
    _COUNTRIES = {
        'Afeganistão': 'AFG',
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
        'Emirados Árabes Unidos': 'EAU',
        'Eslováquia': 'EVQ',
        'Eslovênia': 'EVN',
        'Gana': 'GNA',
        'Gâmbia': 'GMB',
        'Granada': 'GRN',
        'Haiti': 'HTI',
        'Iraque': 'IRQ',
        'Mauritânia': 'MRT',
        'Maurício': 'MRC',
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
        'St Lucia': 'SLU',
        'St Kitts and Nevis': 'SKN',
        'Vietnã': 'VTM',
        'Zimbábue': 'ZBW'
    }

    def __init__(self):
        super().__init__('espn',
                         'https://www.espn.com.br/futebol/time/elenco/_/id/',
                         self._COUNTRIES)

    def get_coach(self, equipa_file: str, season: str) -> list:
        return '' # not available on espn provider

    def assemble_uri(self, team_id: str, season: str) -> str:
        return f'{self._base_url}{team_id}/season/{season}' if season else \
            f'{self._base_url}{team_id}'

    def parse_reply(self, reply: str) -> list | None:
        ret = findall(r'(\"athletes\":[\'\[\{"\w:,\/\.\d~\-\s\}\\p{L}\(\)]+\])',
                      reply.text)

        try:
            goalkeepers = loads('{' + ret[0] + '}')
            others = loads('{' + ret[1] + '}')

            return self._parse_players(goalkeepers.get('athletes') + \
                                       others.get('athletes'))
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
        return player.get('name') \
            if len(player.get('name')) <= self._MAX_NAME_SIZE \
            else player.get('shortName')

    def _parse_players(self, data: list) -> list:
        players = []

        for player in data:
            if not player.get('ctz'): # ignore players with unknown country
                continue

            # TODO: discard players with unmaped countries

            players.append(
                Player(
                    name=self._get_player_name(player),
                    position=player.get('position'),
                    country=self.get_country(player.get('ctz')),
                    appearances=player.get('appearances', 0)
                )
            )

        return players
