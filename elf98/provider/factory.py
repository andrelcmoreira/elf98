from provider.espn import EspnProvider
from provider.transfermarkt import TransfermarktProvider


def create(
    provider_name: str
) -> EspnProvider | TransfermarktProvider | None:
    match provider_name:
        case 'espn':
            return EspnProvider()
        case 'transfermarkt':
            return TransfermarktProvider()

    return None
