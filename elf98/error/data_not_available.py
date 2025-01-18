
class EquipaDataNotAvailable(Exception):

    def __init__(self, equipa: str):
        super().__init__(f"the specified provider has no data for equipa '{equipa}'!")
