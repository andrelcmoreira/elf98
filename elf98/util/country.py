from unidecode import unidecode


# FIXME: the name of the countries are provider specific
_COUNTRIES = {
    'África do Sul': 'AFS',
    'Cape Verde Islands': 'CAV',
    'Cazaquistão': '',
    'Chade': 'CHD',
    'Congo (Brazavile)': 'CNG',
    'Costa do Marfim': 'CMF',
    'Costa Rica': 'CRC',
    'Chile': 'CHL',
    'China': 'CHN',
    'China PR': 'CHN',
    'Chipre': 'CHP',
    'Curaçao': '',
    'Czechia': 'RCH',
    'Coreia do Sul': 'CRS',
    'Egito': 'EGT',
    'Eritreia': '',
    'Eslováquia': 'EVQ',
    'Eslovênia': 'EVN',
    'Gana': 'GNA',
    'Gâmbia': 'GMB',
    'Granada': 'GRN',
    'Irã': '',
    'Kosovo': '',
    'Liechtenstein': '',
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


def get_country(country: str) -> str:
    return _COUNTRIES[country] \
        if country in _COUNTRIES \
        else unidecode(country[0:3]).upper()
