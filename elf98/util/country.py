from unidecode import unidecode


def get_country(country):
    cnt = country[0:3].upper()

    match cnt:
        case 'EGI': return 'EGT'
        case 'GAN': return 'GNA'
        case 'VEN': return 'VNZ'
        case 'REP': return 'RCH'

    return unidecode(cnt)
