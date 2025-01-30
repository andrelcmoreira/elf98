from command.update import UpdateEquipa
from view.base_view import BaseView

from error.not_provided import EquipaNotProvided
from error.data_not_available import EquipaDataNotAvailable


class UpdateEquipaView(BaseView):

    def __init__(self, equipa_file: str, provider: str, season: str):
        self._equipa = equipa_file
        self._prov = provider
        self._season = season

    def show(self):
        try:
            cmd = UpdateEquipa(self._equipa, self._prov, self._season)

            cmd.run()
        except (EquipaNotProvided, EquipaDataNotAvailable) as e:
            print(e)
