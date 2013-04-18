#-------------------------------------------------------------------------------
# Name:        writer.py
# Purpose:     Writer object
#
# Author:      Clay
# License:     MIT
#-------------------------------------------------------------------------------
from prettytable import PrettyTable as Table
from pathlib import Path
from webbrowser import open_new_tab
from mechcanary.sorttable import sorttable_script
import logging
log = logging.getLogger('canary')

html_template = (
"""
<!DOCTYPE html>
<script src="sorttable.js"></script>
<html>
<body>
{}
</body>
</html>
""")

construct_heading = "<h2>{}</h2>".format
construct_paragraph = "<p>{}</p>".format
construct_script = '<script src="{}"></script>'.format

def construct_section(name, categories, rows):
    heading = construct_heading(name)
    table = construct_table(categories, rows)
    section = construct_paragraph(heading + table)
    return section

def construct_table(categories, rows):
    table = Table(categories)
    for row in rows:
        table.add_row(row)
    result = table.get_html_string(format = True, attributes = {'class':'sortable'})
    result = result.replace('rules="cols"', 'rules="all"')
    return result

class Writer:

    def __init__(self, options):
        self.output_path = Path(options.get("Writer", "Output path"))
        self.open_browser = options.getboolean("Writer", "Open Browser")
        self.script_path = self.output_path.parent().join('sorttable.js')
        self.data = {}

    def write(self):
        s = ""
        for test, result in self.data.items():
            s += construct_section(str(test), result[0], result[1:])

        output = html_template.format(s)

        with open(str(self.output_path), 'w') as file:
            file.write(output)

        with open(str(self.script_path), 'w') as script_file:
            script_file.write(sorttable_script)

    def finish(self):
        if self.open_browser:
            open_new_tab(self.output_path.absolute().as_uri())


