#-------------------------------------------------------------------------------
# Name:        mechcanary.py
# Purpose:     Main mechcanary Program Module
#
# Author:      Clay
# License:     MIT
#-------------------------------------------------------------------------------
import logging
from multiprocessing import freeze_support
from mechcanary.options import load_options
from mechcanary.filer import Filer
from mechcanary.collator import Collator
from mechcanary.writer import Writer
from mechcanary.tests import *
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M %p')
log = logging.getLogger('canary')
log.setLevel(logging.INFO)

def main():
    log.info("Starting up MechCanary")

    # Load configuration
    log.info("Loading configuration and settings...")
    options = load_options()

    # Initialize main objects
    log.info("Initializing core components...")
    filer = Filer(options)
    collator = Collator(options)
    writer = Writer(options)

    # Initialize test objects
    log.info("Intializing test components...")
    tests = [FileExecutionTest, FileInfoTest]
    collator.add_tests(tests)

    # Gather the files
    log.info("Gathering files...")
    files = filer.gather_files()
    collator.add_files(files)

    # Start test execution and data processing
    log.info("Starting tests...")
    results = collator.run_tests()

    # Write the data
    log.info("Writing output...")
    writer.data.update(results)
    writer.write()

    log.info("Analysis complete.")
    filer.finish()
    collator.finish()
    writer.finish()

    inp = input("Press any key to exit.")
    exit()


if __name__ == '__main__':
    freeze_support()
    main()
