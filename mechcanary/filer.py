#-------------------------------------------------------------------------------
# Name:        filer.py
# Purpose:     Gathers files
#
# Author:      Clay
# License:     MIT
#-------------------------------------------------------------------------------
from pathlib import Path
import logging
log = logging.getLogger('canary')

class Filer:

    def __init__(self, options):
        self.target_path = options.get("Filer", "Target path")
        self.target_name = options.get("Filer", "Target file") + ".java"
        self.depth_limit = options.getint("Filer", "Folder Depth Limit")
        self.file_limit = options.getint("Filer", "File Limit")

    def gather_files(self):
        directories = [Path(self.target_path)]
        files = []
        while len(directories) > 0:
            if len(directories) > self.depth_limit:
                break
            if len(files) > self.file_limit:
                break

            path = directories.pop()
            for item in path:
                if item.is_file():
                    if item.name == self.target_name:
                        files.append(item)
                elif item.is_dir():
                    directories.append(item)
        return files

    def finish(self):
        pass