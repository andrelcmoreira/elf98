from provider.base_provider import BaseProvider


class TransfermarktProvider(BaseProvider):

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
        super().__init__('transfermarkt',
                         'https://www.espn.com.br/futebol/time/elenco/_/id/',
                         self._COUNTRIES)

    def assemble_uri(self, team_id: str, season: str) -> str:
        pass

    def parse_reply(self, reply: str) -> list | None:
        pass

    def select_players(self, player_list: list) -> list:
        pass
