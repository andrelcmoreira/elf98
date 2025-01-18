from argparse import Namespace

from command.view import ViewEquipa
from command.update import UpdateEquipa
from command.bulk_update import BulkUpdate


class CommandFactory:

    @staticmethod
    def create(
        args: Namespace
    ) -> ViewEquipa | UpdateEquipa | BulkUpdate | None:
        if not args:
            return None

        if args.view_equipa:
            return ViewEquipa(args.view_equipa)
        if args.update_equipa:
            return UpdateEquipa(args.update_equipa, args.provider, args.season)
        if args.bulk_update:
            return BulkUpdate(args.provider, args.bulk_update, args.season)

        return None
