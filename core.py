# The core functions for wb2
import sys, json, os

# Store all the commands
commands = []
user_settings = None
project_settings = None


# Add a command to the registry
def add_command(command):
    commands.append(command)


def run_command(name):
    ran = False
    for command in commands:
        if command.name() == name:
            command.run(sys.argv[2:])
            ran = True
    if ran is False:
        print("No matching commands.")


def command_help(name):
    for command in commands:
        if command.name() == name:
            command.help(sys.argv[2:])


def print_help():
    print("Usage: wb2 <command>")
    print("")
    print("Commands:")
    longest_name = 0;
    for command in commands:
        if len(command.name()) > longest_name:
            longest_name = len(command.name())

    for command in commands:
        if not command.name().startswith("-"):
            print(" " + pad_string(command.name(), longest_name + 4) + command.description())
    print("Use \"wb2 <command> -help\" for help with specific commands")


def pad_string(text, length):
    padding_length = length - len(text)
    padding = ""
    for x in range(padding_length):
        padding = padding + " "
    return text + padding


def get_user_settings():
    global user_settings
    if user_settings is None:
        try:
            with open(os.path.expanduser("~/.wb2/user.json"), "r") as file:
                raw_data = file.read()
                user_settings = json.loads(raw_data)
                file.close()
        except FileNotFoundError:
            pass
            user_settings = {}
    return user_settings


def set_user_settings(settings):
    global user_settings
    user_settings = settings
    with open(os.path.expanduser("~/.wb2/user.json"), "w+") as file:
        file.write(json.dumps(user_settings))
        file.close()


def get_project_settings():
    global project_settings
    if project_settings is None:
        try:
            with open("wb2.json") as file:
                raw_data = file.read()
                project_settings = json.loads(raw_data)
                file.close()
        except FileNotFoundError:
            pass

    return project_settings
