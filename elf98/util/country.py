from unidecode import unidecode


_COUNTRIES = {
    'África do Sul': 'AFS',
    'Cape Verde Islands': 'CAV',
    'Chade': 'CHD',
    'Congo (Brazavile)': 'CNG',
    'Costa do Marfim': 'CMF',
    'Chile': 'CHL',
    'Czechia': 'RCH',
    'Coreia do Sul': 'CRS',
    'IRA': '', # ira
    'Egito': 'EGT',
    'Eslovênia': 'EVN',
    'Gana': 'GNA',
    'PAI': '', # walles
    'USA': 'EUA',
    'Venezuela': 'VNZ',
    'República da Sérvia': 'SER'
}


def get_country(country):
    return _COUNTRIES[country] \
        if country in _COUNTRIES \
        else unidecode(country[0:3]).upper()
