from unidecode import unidecode


# TODO: missing 'ira' flag on 'FLAGS' dir
_COUNTRIES = {
    'AFR': 'AFS',
    'CAP': 'CAV',
    'CHA': 'CHD',
    'CHI': 'CHL',
    'EGI': 'EGT',
    'ESL': 'EVN',
    'GAN': 'GNA',
    'VEN': 'VNZ',
    'REP': 'RCH'
}


def get_country(country):
    cnt = unidecode(country[0:3]).upper()

    return _COUNTRIES[cnt] if cnt in _COUNTRIES else cnt
