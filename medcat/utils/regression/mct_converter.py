
import argparse
import logging
import os
from pathlib import Path

from medcat.utils.regression.converting import medcat_export_json_to_regression_yml


logger = logging.getLogger(__name__)


def main(mct_export: str, target: str, overwrite: bool = False) -> None:
    if not overwrite and os.path.isfile(target):
        raise ValueError("Not able to overwrite an existingfile, "
                         "pass '--overwrite' to force an overwrite")
    logger.info(
        "Starting to convert export JSON to YAML from file %s", mct_export)
    yaml = medcat_export_json_to_regression_yml(mct_export)
    logger.debug("Conversion successful")
    logger.info("Saving writing data to %s", target)
    with open(target, 'w') as f:
        f.write(yaml)
    logger.debug("Done saving")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file', help='The MedCATtrainer export file', type=Path)
    parser.add_argument('target', help='The Target YAML file', type=Path)
    parser.add_argument('--silent', '-s', help='Make the operation silent (i.e ignore console output)',
                        action='store_true')
    parser.add_argument('--verbose', '-debug', help='Enable debug/verbose mode',
                        action='store_true')
    parser.add_argument(
        '--overwrite', help='Overwrite the target file if it exists', action='store_true')
    args = parser.parse_args()
    if not args.silent:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel('INFO')
    if args.verbose:
        from checking import logger as checking_logger
        checking_logger.addHandler(logging.StreamHandler())
        checking_logger.setLevel('DEBUG')
    main(args.file, args.target, overwrite=args.overwrite)
