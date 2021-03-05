from core import *

from core import add_command


class UpdateCommand:

    @staticmethod
    def name():
        return "--update"

    @staticmethod
    def description():
        return "Run updates on wb2."

    @staticmethod
    def help():
        pass

    @staticmethod
    def run(args):
        print("Starting wb2 update")


mainFolder = sys.argv[0][0:sys.argv[0].rfind("/")]
with open(mainFolder + "/use-updater.txt") as file:
    contents = file.read()
    file.close()
    if contents == "true":
        updateCommand = UpdateCommand()
        add_command(updateCommand)