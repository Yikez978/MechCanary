import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

setup(  name = "MechCanary",
        version = "0.1",
        description = "MechCanary File Analyzer",
        options = {"build_exe": build_exe_options},
        executables = [Executable("MechCanary.py"), Executable("mechcanary/options.py")])
