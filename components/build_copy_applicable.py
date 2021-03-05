import os
from components.build import add_build_command_step


class BuildCopyApplicable:

    @staticmethod
    def copy_files(dir):
        files = os.listdir(dir)
        print(files)

    @staticmethod
    def run(taskset):
        print("copying relevant files...")
        BuildCopyApplicable.copy_files(".")

    @staticmethod
    def priority():
        return 1


add_build_command_step(BuildCopyApplicable())
