from provider.espn import EspnProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name):
        if provider_name == 'espn':
            return EspnProvider()

        return None
