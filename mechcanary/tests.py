#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Clay
#
# Created:     09/04/2013
# Copyright:   (c) Clay 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from subprocess import Popen as open_process, PIPE
from difflib import SequenceMatcher

class Test:
    def __init__(self, config):
        pass

class FileInfoTest(Test):
    name = "File Information"
    heading = ['File', 'User ID', 'Group ID', 'Size (kb)']

    def process(self, data, executor):
        s = [self.heading]
        for _file in data:
            uid = _file.stat().st_uid
            gid = _file.stat().st_gid
            size = _file.stat().st_size
            s.append([str(_file), uid, gid, size])
        return s

class FileExecutionTest(Test):
    name = "File Execution Test"
    heading = ['File', 'Compiled', 'Ran']

    def __init__(self, config):
        # Content Matching
        content_file = config.get("Collator", "Sample Content File")
        if content_file != "":
            self.heading.append("Content Similarity")
            with open(content_file, 'r') as _file:
                self.content = _file.read()
                self.compare_content = True
        else:
            self.content = ""
            self.compare_content = False

        # Output Matching
        output_file = config.get("Collator", "Sample Output File")
        if output_file != "":
            self.heading.append("Output Similarity")
            with open(output_file, 'r') as _file:
                self.output = _file.read()
                self.compare_output = True
        else:
            self.input = ""
            self.compare_output = False

        # Program input
        input_file = config.get("Collator", "Program Input File")
        if input_file != "":
            with open(input_file, 'r') as _file:
                self.input = _file.read()
        else:
            self.input = ""

    def process(self, data, executor):
        results = [self.heading]
        temp = {}

        for element in data: # Submit all the files to be processed to the executor
            temp[element] = executor.submit(file_execution_test, self, element)

        for key, result in temp.items():
            compiler_info, program_info, match_info = result.result()
            row = [key, (compiler_info[2] == 0), (program_info[2] == 0)]

            if self.compare_content:
                row.append(match_info[0])

            if self.compare_output:
                row.append(match_info[1])

            results.append(row)
        return results

def file_execution_test(config, filepath):
    compiler_info = (None, None, None)
    program_info = (None, None, None)
    content_similarity = None
    output_similarity = None

    compiler_info = compile_file(config, filepath)

    if config.compare_content:
        with open(str(filepath), 'r') as _file:
            content = _file.read()
            ratio = SequenceMatcher(a=content, b=config.content).ratio()
            content_similarity = round(ratio, 4)*100

    if compiler_info[2] == 0:
        program_info = run_program(config, filepath)
        if (config.compare_output) and (program_info[2] == 0):
            output = program_info[0]
            ratio = SequenceMatcher(a=output, b=config.output).ratio()
            output_similarity = round(ratio, 4)*100
    similarity = (content_similarity, output_similarity)

    return (compiler_info, program_info, similarity)


def compile_file(config, filepath):
    cmd = 'javac "{}"'.format(str(filepath))
    process = open_process(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    st_output, st_error = process.communicate(timeout = 30)
    code = process.returncode
    return (st_output, st_error, code)

def run_program(config, filepath):
    classpath = str(filepath).strip(filepath.name)
    classfile = filepath.name.strip(".java")
    cmd = 'java  {}'.format(classfile)
    process = open_process(cmd, cwd=classpath, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    st_output, st_error = process.communicate(bytes(config.input, 'UTF-8'), timeout = 30)
    code = process.returncode
    return (st_output, st_error, code)