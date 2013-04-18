#-------------------------------------------------------------------------------
# Name:        collator.py
# Purpose:     Runs tests with file data
#
# Author:      Clay
# License:     MIT
#-------------------------------------------------------------------------------
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging
log = logging.getLogger('canary')

class Collator:

    def __init__(self, options):
        self.process_limit = options.getint("Collator", "Process limit")
        self.execution_args = options.get("Collator", "Execution arguments")
        self.config = options

        self.test_executor = ThreadPoolExecutor(self.process_limit)
        self.task_executor = ProcessPoolExecutor(self.process_limit)

        self.datas = []
        self.tests = []

    def add_tests(self, tests):
        log.debug("Adding tests {}".format(str(tests)))
        self.tests.extend(tests)

    def add_files(self, files):
        log.debug("Adding files {}".format(str(files)))
        self.datas.extend(files)

    def run_tests(self):
        log.info("Runnng tests.")
        temp_results = {}
        final_results = {}

        for test_class in self.tests:
            log.info("Submitting test {}".format(str(test_class)))
            test = test_class(self.config)
            future = self.test_executor.submit(
                test.process, self.datas, self.task_executor
                )
            temp_results[test.name] = future

        for test_name, future in temp_results.items():
            final_results[test_name] = future.result()

        return final_results

    def finish(self):
        pass