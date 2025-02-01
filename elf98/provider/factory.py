from provider.espn import EspnProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str) -> EspnProvider | None:
        if provider_name == 'espn':
            return EspnProvider()

        return None
