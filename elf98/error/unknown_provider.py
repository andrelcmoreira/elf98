
class UnknownProvider(Exception):

    def __init__(self, provider_name):
        super().__init__(f"Unkwnown provider '{provider_name}'!")
