from command.command import Command
from provider.factory import ProviderFactory
from error.unknown_provider import UnknownProvider


class BulkUpdate(Command):

    def __init__(self, provider):
        self._prov = ProviderFactory.create(provider)

        if not self._prov:
            raise UnknownProvider(provider)

    def run(self):
        pass
