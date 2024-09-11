
class EquipaNotFound(Exception):

    def __init__(self, equipa_name: str):
        super().__init__(f"Equipa '{equipa_name}' not found!")
