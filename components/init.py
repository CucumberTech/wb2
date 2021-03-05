import time, json, jsbeautifier

from components.repograbber import load_resource
from core import *
import os


class InitCommand:

    @staticmethod
    def name():
        return "init"

    @staticmethod
    def description():
        return "Setup a wb2 project."

    @staticmethod
    def help(args):
        print("wb2 init")
        print("")
        print("Basics:")
        print(
            "The init command will setup a wb2 workspace with a configuration file and file structure based on the archetype selected")
        print("")
        print("Modifiers:")
        print(" -s, --silent                 Run the command without any user input (silent mode)")
        print(" --yes                        Don't display confirmation dialogs. Not necessary if in silent")
        print(" name=<name>                  Supply the project name, it will not be asked")
        print(" description=<description>    Supply the description, it will not be asked")
        print(" author=<author>              Supply the author, it will not be asked")
        print(" domain=<doman>               Supply the domain, it will not be asked")
        print(" archetype=<archetype>        Supply the archetype, it will not be asked")
        print("")
        print("Additional Information:")
        print("When running in silent mode, you must supply the archetype. All other properties don't need to be set.")

    @staticmethod
    def process_files(file, parent, flags):
        if file["type"] == "folder":
            if len(file["flags"]) > 0:
                flags.append({"file": parent + file["name"], "flags": file["flags"]})
            try:
                os.mkdir(parent + file["name"])
            except FileExistsError:
                pass
            new_parent = parent + file["name"] + "/"
            for subfile in file["files"]:
                InitCommand.process_files(subfile, new_parent, flags)
        if file["type"] == "file":
            if len(file["flags"]) > 0:
                flags.append({"file": parent + file["name"], "flags": file["flags"]})
            with open(parent + file["name"], "w+") as output:
                output.write(file["content"])
                output.close()
        return flags

    @staticmethod
    def run(args):
        # Declare Variables we will be using
        silent = False
        confirm = True
        name = ""
        description = ""
        author = ""
        domain = ""
        archetype_name = ""
        # Parse Command Line Args
        if "--silent" in args or "-s" in args:
            silent = True
        if "--yes" in args:
            confirm = False
        for arg in args:
            if arg.startswith("name="):
                name = arg[5:]
            if arg.startswith("description="):
                description = arg[12:]
            if arg.startswith("author="):
                author = arg[7:]
            if arg.startswith("domain="):
                domain = arg[7:]
            if arg.startswith("archetype="):
                archetype_name = arg[10:]

        # Load user settings
        userset = get_user_settings()
        if not "name" in userset and not silent:
            print("Your user settings aren't configured yet. Let's get some basics setup.")
            print("What's your name? We will use this as a default for creating projects.")
            userset["name"] = input()
            print("Cool! Saving...")
            set_user_settings(userset)
            time.sleep(1)

        project = get_project_settings()
        if project is not None:
            print("wb2 is already setup in this directory.")
            exit(1)


        folderName = os.getcwd()[os.getcwd().rfind("/") + 1:]
        if not silent:
            print("wb2 project setup")
            print("")

        if not silent and name == "":
            print("What's the project name? [" + folderName + "]")
            name = input()
            if name == "":
                name = folderName

        if not silent and description == "":
            print("Enter a brief description of your project.")
            description = input()

        if not silent and author == "":
            print("Who is the author of this project? [" + userset["name"] + "]")
            author = input()
            if author == "":
                author = userset["name"]

        if not silent and domain == "":
            print("What is a domain for this project?")
            domain = input()

        if not silent and archetype_name == "":
            print("What archetype would you like to use? [standard]")
            archetype_name = input()
            if archetype_name == "":
                archetype_name = "standard"

        if not silent and confirm:
            print("Properties:")
            print(" name: " + name)
            print(" description: " + description)
            print(" author: " + author)
            print(" domain: " + domain)
            print(" archetype: " + archetype_name)
            print("Is this correct? [ENTER] to proceed or Ctrl-C to cancel")
            input()

        if domain == "":
            if not silent:
                print("No domain entered")
            exit(1)


        if not silent:
            print("Setting up workspace...")

        # Load Archetype data
        archetype = load_resource("archetype", archetype_name)
        if archetype is None:
            if not silent:
                print("Archetype not found.")
            exit(1)

        workspaceFile = {}
        # Set Project Metadata
        workspaceFile["project"] = {}
        workspaceFile["project"]["name"] = name
        workspaceFile["project"]["description"] = description
        workspaceFile["project"]["author"] = author

        # Setup custom repos
        workspaceFile["repositories"] = []
        for repo in archetype["default_repositories"]:
            workspaceFile["repositories"].append(repo)

        # Setup the domain
        workspaceFile["domains"] = []
        workspaceFile["domains"].append({})
        workspaceFile["domains"][0]["name"] = domain
        workspaceFile["domains"][0]["archetype"] = archetype_name
        workspaceFile["domains"][0]["dependencies"] = []
        for dependency in archetype["default_dependencies"]:
            workspaceFile["domains"][0]["dependencies"].append(dependency)

        workspaceFile["domains"][0]["tasks"] = archetype["default_tasks_config"]

        # Setup tasks
        workspaceFile["tasks"] = {}

        with open("wb2.json", "w+") as file:
            file.write(jsbeautifier.beautify(json.dumps(workspaceFile)))
            file.close()

        try:
            os.mkdir(".wb2")
        except FileExistsError:
            pass

        try:
            os.mkdir(".wb2/" + domain)
        except FileExistsError:
            pass

        with open("./.wb2/" + domain + "/archetype.json", "w+") as file:
            file.write(json.dumps(archetype))
            file.close()

        try:
            os.mkdir(domain)
        except FileExistsError:
            pass

        # Create Default Files
        flags = []
        for file in archetype["default_file_structure"]:
            flags = InitCommand.process_files(file, "./" + domain +"/", flags)

        with open("./.wb2/" + domain + "/flags.json", "w+") as file:
            file.write(json.dumps(flags))
            file.close()

        if not silent:
            print("Workspace setup.")


initCommand = InitCommand()
add_command(initCommand)
