import argparse, os, logging

from model import Dataset
from parsers import parse
from simulation import run_simulation

VERSION = 0.1

# TODO: User-specified logging level.
logger = logging.getLogger(__name__)

def print_version():
    print "PyNewhall {}".format(VERSION)

def run_model(file_or_directory):
    # Determine if input is single or multi run.
    if os.path.isfile(file_or_directory):
        # Single run mode, open file and run.
        logger.debug("Importing file: {}".format(file_or_directory))
        input_file = open(file_or_directory, "r")

        # Parse into dataset.
        dataset = parse(input_file)
        logger.debug("Built dataset: {}".format(dataset.get("name")))

        # Run the model and catch the results.
        results = run_simulation(dataset)
        logger.debug("Simulation run complete, results: {}".format(results))

        # Store report from model invocation on dataset.
        # Check output selections.
        # Write output file, close.
        exit(-1)
    elif os.path.isdir(file_or_directory):
        logger.debug("WRITE ME!")
        exit(-1)
    else:
        # Not a file or directory, exit.
        raise Exception("Not a file or directory: {}".format(file_or_directory))

if __name__ == "__main__":
    description = "PyNewhall {} - CLI Interface for the Newhall Simulation Model".format(
        VERSION)

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--version", help="show version and exit", action="store_true")
    parser.add_argument("--run", help="run model for argument file or directory (batch mode)")
    parser.add_argument("--debug", help="report extra debugging information while running", 
        action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.version:
        # Print version and exit succesfully.
        print_version()
        exit(0)

    if args.run:
        try:
            # Attempt to run the model.
            run_model(args.run)
        except Exception as ex:
            # Report exception message.
            print ex
            exit(1)
        exit(0)
    else:
        print "No datasets specified, exiting.  Use --help for more details."
