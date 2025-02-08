from provider.espn import EspnProvider


def create(provider_name: str) -> EspnProvider | None:
    if provider_name == 'espn':
        return EspnProvider()

    return None
