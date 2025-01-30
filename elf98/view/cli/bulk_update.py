from command.bulk_update import BulkUpdate
from view.base_view import BaseView


class BulkUpdateView(BaseView):

    def __init__(self, equipa_dir: str, provider: str, season: str):
        self._equipa_dir = equipa_dir
        self._prov = provider
        self._season = season

    def show(self):
        pass
        #try:
        #    pass
        #except (EquipaNotFound, EquipaDataNotAvailable) as e:
        #    raise e
        #cmd = BulkUpdate(self._equipa_dir, self._prov, self._season)

        #cmd.run()
