#!/usr/bin/python3
import argparse

from libboutique.publisher.progress_publisher import ProgressPublisher
from libboutique.handler.command_handler import CommandHandler


def show_progress(package, progress):
    # print(package)
    print(progress)


if __name__ == "__main__":
    command_handler = CommandHandler(origin="cli", callback_subscribe=show_progress)

    commands = {
        "install_app=": command_handler.install_package,
        "remove_app=": command_handler.remove_package,
        "query=": None,
    }

    args = argparse.ArgumentParser()
    groups = args.add_mutually_exclusive_group()
    groups.add_argument("--install-app=", type=str, help="Install specified package")
    groups.add_argument("--remove-app=", type=str, help="Remove specified package")
    groups.add_argument("--query=", type=str, help="Return list of available package")  # TODO Work on the wording
    cli_input = args.parse_args()

    cli_dict = vars(cli_input)

    for key, value in cli_dict.items():
        if value is not None:
            commands.get(key)(name=value)
            break
