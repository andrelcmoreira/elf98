
class EquipaDataNotAvailable(Exception):

    def __init__(self, team_id: str):
        super().__init__(f"the specified provider has no data for ID '{team_id}'!")
