from unidecode import unidecode


# TODO: use full country name as key
_COUNTRIES = {
    'AFR': 'AFS',
    'CAP': 'CAV',
    'CHA': 'CHD',
    'CON': 'CNG',
    'COS': 'CMF',
    'CHI': 'CHL',
    'CZE': 'RCH',
    'COR': 'CRS',
    'IRA': '', # ira
    'EGI': 'EGT',
    'ESL': 'EVN',
    'GAN': 'GNA',
    'PAI': '', # walles
    'USA': 'EUA',
    'VEN': 'VNZ',
    'REP': 'RCH'
}


def get_country(country):
    cnt = unidecode(country[0:3]).upper()

    return _COUNTRIES[cnt] if cnt in _COUNTRIES else cnt
