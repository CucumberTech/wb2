# This file loads any and all modules

# Imports
import importlib
import os
import sys

# determine the modules directory
appFile = sys.argv[0]
componentsDir = appFile[0:appFile.rfind("/")] + "/components"
sys.path.append(componentsDir)

# Load any applicable modules
files = os.listdir(componentsDir)
for file in files:
    if file.endswith("py") and not file.startswith("__"):
        importlib.import_module(file[0:file.index(".")])

# Load any project modules
sys.path.append("./wb2/components")
try:
    files = os.listdir("./wb2/components")
    for file in files:
        if file.endswith("py") and not file.startswith("__"):
            importlib.import_module(file[0:file.index(".")])
except FileNotFoundError:
    pass
