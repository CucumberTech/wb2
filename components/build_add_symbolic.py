from components.build import add_build_command_step


class BuildAddSymbolic:
    @staticmethod
    def run(taskset):
        print("adding symbolic links...")

    @staticmethod
    def priority():
        return 1000


add_build_command_step(BuildAddSymbolic())
