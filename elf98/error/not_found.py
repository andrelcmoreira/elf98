
class EquipaNotFound(Exception):

    def __init__(self, equipa_name):
        super().__init__(f"Equipa '{provider_name}' not found!")
