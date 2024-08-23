from unidecode import unidecode


def get_country(country):
    cnt = country[0:3].upper()

    match cnt:
        # TODO: missing eslovenia flag on 'FLAGS' dir
        # TODO: missing iraq flag on 'FLAGS' dir
        case 'AFR': return 'AFS'
        case 'CAP': return 'CAV'
        case 'CHA': return 'CHD'
        case 'CHI': return 'CHL'
        case 'EGI': return 'EGT'
        case 'GAN': return 'GNA'
        case 'VEN': return 'VNZ'
        case 'REP': return 'RCH'

    return unidecode(cnt)
