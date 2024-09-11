
class UnknownProvider(Exception):

    def __init__(self, provider_name: str):
        super().__init__(f"Unkwnown provider '{provider_name}'!")
