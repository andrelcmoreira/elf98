from argparse import Namespace

from command.bulk_update import BulkUpdate
from command.update import UpdateEquipa
from command.view import ViewEquipa


class CommandFactory:

    @staticmethod
    def create(
        args: Namespace
    ) -> ViewEquipa | UpdateEquipa | BulkUpdate | None:
        if args.view_equipa:
            return ViewEquipa(args.view_equipa)
        if args.update_equipa:
            return UpdateEquipa(args.update_equipa, args.provider, args.season)
        if args.bulk_update:
            return BulkUpdate(args.bulk_update, args.provider, args.season)

        return None
