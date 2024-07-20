from command.view import ViewEquipa
from command.update import UpdateEquipa


class CommandFactory:

    @staticmethod
    def create(args):
        if args.view:
            return ViewEquipa(args.equipa_file)
        if args.update:
            return UpdateEquipa(args.equipa_file, args.provider)
        if args.bulk_update:
            return None # TODO

        return None
