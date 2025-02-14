from unidecode import unidecode


# FIXME: the name of the countries are provider specific
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


def get_country(country: str) -> str:
    return _COUNTRIES[country] \
        if country in _COUNTRIES \
        else unidecode(country[0:3]).upper()
