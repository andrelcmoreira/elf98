from unidecode import unidecode


# FIXME: the name of the countries are provider specific
_COUNTRIES = {
    'África do Sul': 'AFS',
    'Cape Verde Islands': 'CAV',
    'Chade': 'CHD',
    'Congo (Brazavile)': 'CNG',
    'Costa do Marfim': 'CMF',
    'Costa Rica': 'CRC',
    'Chile': 'CHL',
    'Czechia': 'RCH',
    'Coreia do Sul': 'CRS',
    'Irã': '',
    'Kosovo': '',
    'Egito': 'EGT',
    'Eslovênia': 'EVN',
    'Gana': 'GNA',
    'Gâmbia': 'GMB',
    'País de Gales': '',
    'USA': 'EUA',
    'Venezuela': 'VNZ',
    'Republic of Ireland': 'IRL',
    'República da Sérvia': 'SER'
}


def get_country(country):
    return _COUNTRIES[country] \
        if country in _COUNTRIES \
        else unidecode(country[0:3]).upper()
