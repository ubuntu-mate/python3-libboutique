import argparse

# from libboutique.publisher.progress_publisher import ProgressPublisher
from libboutique.services.curated_app_service import CuratedAppService
from libboutique.handlers.package_command_handler import PackageCommandHandler


def show_progress(package, progress):
    print(package)
    print(progress)


def main():
    command_handler = PackageCommandHandler(callback_subscribe=show_progress)
    curated_apps_service = CuratedAppService()

    commands = {
        "install-app=": command_handler.install_package,
        "remove-app=": command_handler.remove_package,
        "query=": None,
        "rebuild-index": curated_apps_service.build_index
    }

    args = argparse.ArgumentParser()
    groups = args.add_mutually_exclusive_group()
    groups.add_argument("--install-app=", type=str, help="Install specified package")
    groups.add_argument("--remove-app=", type=str, help="Remove specified package")
    groups.add_argument("--query=", type=str, help="Return list of available package")  # TODO Work on the wording
    groups.add_argument("--rebuild-index", type=bool, help="Rebuild the index of curated applications")
    cli_input = args.parse_args()

    cli_dict = vars(cli_input)

    for key, value in cli_dict.items():
        if value is not None:
            print(value)
            commands.get(key)(name=value)
            break
