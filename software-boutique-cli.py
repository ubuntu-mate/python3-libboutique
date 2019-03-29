#!/usr/bin/python3
import argparse

from libboutique.snap.snap_service import SnapService


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    groups = args.add_mutually_exclusive_group()
    groups.add_argument('--install-app=', type=str, help="Install specified package")
    groups.add_argument('--remove-app=', type=str, help="Remove specified package")
    groups.add_argument("--query=", type=str, help="Return list of available package") # TODO Work on the wording
    package_name = args.parse_args()
