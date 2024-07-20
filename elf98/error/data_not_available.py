
class EquipaDataNotAvailable(Exception):

    def __init__(self, team_id):
        super().__init__(f"the specified provider has no data for ID '{team_id}'!")
