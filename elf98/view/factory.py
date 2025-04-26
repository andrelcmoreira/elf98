from argparse import Namespace

from view.cli.bulk_update import BulkUpdate
from view.cli.update_equipa import UpdateEquipa
from view.cli.view_equipa import ViewEquipa


def create(
    args: Namespace
) -> ViewEquipa | UpdateEquipa | BulkUpdate | None:
    if args.view_equipa:
        return ViewEquipa(args.view_equipa)
    if args.update_equipa:
        return UpdateEquipa(args.update_equipa, args.provider, args.season_year,
                            args.output_directory)
    if args.bulk_update:
        return BulkUpdate(args.bulk_update, args.provider, args.season_year,
                          args.output_directory)

    return None
