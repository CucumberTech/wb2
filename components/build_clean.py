import os
from components.build import add_build_command_step


class BuildCleanTarget:
    @staticmethod
    def run(taskset):
        print("cleaning...")
        try:
            os.rmdir(taskset["output"])
        except FileNotFoundError:
            pass

    @staticmethod
    def priority():
        return 0


add_build_command_step(BuildCleanTarget())
