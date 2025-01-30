from argparse import Namespace

from view.cli.view_equipa import ShowEquipa
from view.cli.update_equipa import UpdateEquipaView
from view.cli.bulk_update import BulkUpdateView


class ViewFactory:

    @staticmethod
    def create(
        args: Namespace
    ) -> ShowEquipa | UpdateEquipaView | BulkUpdateView | None:
        if args.view_equipa:
            return ShowEquipa(args.view_equipa)
        if args.update_equipa:
            return UpdateEquipaView(args.update_equipa, args.provider, args.season)
        if args.bulk_update:
            return BulkUpdateView(args.bulk_update, args.provider, args.season)

        return None
