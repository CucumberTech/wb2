from core import *

steps = []
stepNumbers = []
stepsOrdered = {}


class BuildCommand:

    @staticmethod
    def name():
        return "build"

    @staticmethod
    def description():
        return "Assemble a configured wb2 project."

    @staticmethod
    def help(args):
        print("wb2 build")
        print("")
        print("Basics:")
        print("The build command assembles production ready files based on the task configuration")
        print("")
        print("Modifiers:")
        print("")

    @staticmethod
    def run(args):
        projset = get_project_settings()
        if projset is None:
            print("No wb2 workspace.")
            exit(1)
        try:
            taskset = projset["tasks"]["build"]
            taskset["output"]
            taskset["extensions"]
        except KeyError:
            print("No Configuration for build task. Nothing to do")
            exit(1)

        # Order steps
        for step in steps:
            if not step.priority() in stepsOrdered:
                stepsOrdered[step.priority()] = []
                stepNumbers.append(step.priority())
            stepsOrdered[step.priority()].append(step)
        stepNumbers.sort()

        for number in stepNumbers:
            for step in stepsOrdered[number]:
                step.run(taskset)


buildCommand = BuildCommand()
add_command(buildCommand)


def add_build_command_step(step):
    steps.append(step)
