from argparse import Namespace
from typing import Optional

from view.cli.bulk_update import BulkUpdate
from view.cli.update_equipa import UpdateEquipa
from view.cli.view_equipa import ViewEquipa


def create(
    args: Optional[Namespace]
) -> BulkUpdate | UpdateEquipa | ViewEquipa | None:
    if not args:
        return None # gui

    if args.view_equipa:
        return ViewEquipa(args.view_equipa)
    if args.update_equipa:
        return UpdateEquipa(args.update_equipa, args.provider, args.season_year,
                            args.output_directory)
    if args.bulk_update:
        return BulkUpdate(args.bulk_update, args.provider, args.season_year,
                          args.output_directory)
