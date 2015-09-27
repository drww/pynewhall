import argparse, os

from model import Dataset
from parsers import parse
from simulation import run_simulation

VERSION = 0.1

def print_version():
    print "PyNewhall {}".format(VERSION)

def run_model(file_or_directory):
    # Determine if input is single or multi run.
    if os.path.isfile(file_or_directory):
        # Single run mode, open file and run.
        print "IMPORTING FILE"
        input_file = open(file_or_directory, "r")
        print input_file

        # Parse into dataset.
        dataset = parse(input_file)
        print "BUILT DATASET"
        print dataset.to_json()

        # Run the model and catch the results.
        print "RUNNING SIMULATION"
        results = run_simulation(dataset)

        # Store report from model invocation on dataset.
        # Check output selections.
        # Write output file, close.
        print "DONE"
        exit(-1)
    elif os.path.isdir(file_or_directory):
        print "IMPLEMENT ME"
        exit(-1)
    else:
        # Not a file or directory, exit.
        raise Exception("Not a file or directory: {}".format(file_or_directory))

# Main interface.
if __name__ == "__main__":
    description = "PyNewhall {} - CLI Interface for the Newhall Simulation Model".format(
        VERSION)

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--version", help="show version and exit.", action="store_true")
    parser.add_argument("--run", help="run model for argument file or directory (batch).")
    args = parser.parse_args()

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
