from argparse import Namespace

from command.view import ViewEquipa
from command.update import UpdateEquipa
from command.bulk_update import BulkUpdate


class CommandFactory:

    @staticmethod
    def create(
        args: Namespace
    ) -> ViewEquipa | UpdateEquipa | BulkUpdate | None:
        if args.view_equipa:
            return ViewEquipa(args.equipa_file)
        if args.update_equipa:
            return UpdateEquipa(args.equipa_file, args.provider)
        if args.bulk_update:
            return BulkUpdate(args.provider, args.equipas_dir)

        return None
