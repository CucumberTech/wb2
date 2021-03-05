from core import add_command


class AboutCommand:

    @staticmethod
    def name():
        return "about"

    @staticmethod
    def description():
        return "Show information about wb2."

    def help(self):
        pass

    @staticmethod
    def run(args):
        print("Web Build 2 (wb2)")
        print("Copyright Cucumber Technology 2021. All Rights Reserved.")
        print("Version 2.1.0")


aboutCommand = AboutCommand()
add_command(aboutCommand)