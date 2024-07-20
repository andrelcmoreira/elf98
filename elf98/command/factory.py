from command.view import ViewEquipa
from command.update import UpdateEquipa


class CommandFactory:

    @staticmethod
    def create(args):
        if args.view:
            return ViewEquipa()
        if args.update:
            return UpdateEquipa()
        if args.bulk_update:
            return None # TODO

        return None
