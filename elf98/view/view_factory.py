from argparse import Namespace

from view.cli.bulk_update import BulkUpdateView
from view.cli.update_equipa import UpdateEquipaView
from view.cli.view_equipa import ViewEquipaView


def create(
    args: Namespace
) -> ViewEquipaView | UpdateEquipaView | BulkUpdateView | None:
    if args.view_equipa:
        return ViewEquipaView(args.view_equipa)
    if args.update_equipa:
        return UpdateEquipaView(args.update_equipa, args.provider,
                                args.season, args.output_directory)
    if args.bulk_update:
        return BulkUpdateView(args.bulk_update, args.provider, args.season,
                              args.output_directory)

    return None
