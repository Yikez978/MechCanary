#-------------------------------------------------------------------------------
# Name:        options.py
# Purpose:     Canary options module
#
# Author:      Clay
# License:     MIT
#-------------------------------------------------------------------------------
from configparser import SafeConfigParser

default_options = {
    "General" : {
        "Tests" : "",
        "Debug" : "False"
        },

    "Filer" : {
        "Target path" : "",
        "Target file" : "",
        "Folder Depth Limit" : "50",
        "File Limit" : "50"
        },

    "Collator" : {
        "Process Limit" : "4",
        "Execution arguments" : "",
        "Program input file" : "",
        "Sample content file" : "",
        "Sample output file" : ""
        },

    "Writer" : {
        "Output Path" : "",
        "Open Browser" : "False"
        }
    }

_config = SafeConfigParser()

def create_options():
    for section in default_options:
        _config.add_section(section)
        for option, value in default_options[section].items():
            _config.set(section, option, value)

    with open("mech-canary.cfg", 'w') as file:
        _config.write(file)

def load_options():
    _config.read('mech-canary.cfg')
    print(_config.sections())
    return _config

if __name__ == "__main__":
    create_options()