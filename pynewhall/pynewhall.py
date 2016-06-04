import argparse, os, logging

from dataset import Dataset
from parsers import parse
from simulation import run_simulation

VERSION = 0.8

logger = logging.getLogger("main")

def print_version():
    print "PyNewhall {}".format(VERSION)

def run_model(file_or_directory, param_map={}):
    # Determine if input is single or multi run.
    if os.path.isfile(file_or_directory):
        # Single run mode, open file and run.
        logger.debug("Importing file: {}".format(file_or_directory))
        input_file = open(file_or_directory, "r")

        # Parse into dataset.
        dataset = parse(input_file)
        logger.debug("Built dataset: {}".format(dataset.get("name")))
        for attribute in sorted(dataset.to_dict().keys()):
            logger.debug("    {} = {}".format(attribute, dataset.get(attribute)))

        # Parse model parameters and call model.
        result = None
        if param_map:
            logger.debug("Running model with custom parameters: {}".format(param_map))
            result = run_simulation(dataset, **param_map)
        else:
            logger.debug("Running model with default parameters.")
            result = run_simulation(dataset)

        # Run complete, return results.
        logger.info("Completed simulation run: {} ({} - {})".format(dataset.get("name"),
            dataset.get("start_year"), dataset.get("end_year")))
        return result
    elif os.path.isdir(file_or_directory):
        # Gather files an directories, and perform a recursive descent
        # into the contents, collecting results from runs.
        root_path = os.path.abspath(file_or_directory)
        dir_files = os.listdir(file_or_directory)
        dir_results = []

        for dir_file in dir_files:
            # Merge results, which may be lists of results, into a single list.
            abs_path = "{}/{}".format(root_path, dir_file)
            dir_results += [run_model(abs_path, param_map)]

        logger.info("Processed {} dataset runs.".format(len(dir_results)))
        return dir_results
    else:
        # Not a file or directory, exit.
        raise Exception("Not a file or directory: {}".format(file_or_directory))

if __name__ == "__main__":
    description = "PyNewhall {} - CLI Interface for the Newhall Simulation Model".format(
        VERSION)

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--version", help="show version and exit", action="store_true")
    parser.add_argument("--debug", help="report extra debugging information while running", action="store_true")
    parser.add_argument("--run", help="input dataset or directory containing several datasets")
    parser.add_argument("--whc", help="override default waterholding capacity (200 mm)", type=float)
    parser.add_argument("--sao", help="override default soil-air offset (2.5 deg C)", type=float)
    parser.add_argument("--amp", help="override default soil-air relationship amplitude (0.66)", type=float)
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
        # Build model run parameters, if any are specified.
        model_params = {}
        if args.whc: model_params["water_holding_capacity"] = args.whc
        if args.sao: model_params["fc"] = args.sao
        if args.amp: model_params["fcd"] = args.amp

        # Run a single dataset or multiple through the model.
        try:
            # Attempt to run the model.
            if model_params:
                logger.info("Using custom parameters for following simulation runs: {}".format(model_params))
            else:
                logger.info("Using simulation model default parameters for following simulation runs.")
            all_results = run_model(args.run, model_params)

            if isinstance(all_results, list):
                for result in all_results:
                    print "\n{}".format(result.to_report())
            else:
                print"\n{}".format(all_results.to_report())
            

        except Exception as ex:
            # Report exception message.
            print ex
            exit(1)
        exit(0)
    else:
        print "No datasets specified, exiting.  Use --help for more details."
