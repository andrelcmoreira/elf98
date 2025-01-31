from command.bulk_update import BulkUpdate
from view.base_view import BaseView


class BulkUpdateView(BaseView):

    def __init__(self, equipa_dir: str, provider: str, season: str):
        self._equipa_dir = equipa_dir
        self._prov = provider
        self._season = season

    def show(self):
        cmd = BulkUpdate(self._equipa_dir, self._prov, self._season, self)

        cmd.run()

    def on_update_equipa(self, equipa_name: str):
        pass

    def on_update_equipa_error(self, error: str):
        print(error)
