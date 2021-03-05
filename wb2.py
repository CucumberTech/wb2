from core import *
from components import *

if len(sys.argv) == 1:
    print_help()

elif len(sys.argv) > 1:
    if "-help" in sys.argv:
        command_help(sys.argv[1])
    else:
        run_command(sys.argv[1])
