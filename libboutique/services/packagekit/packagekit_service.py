from typing import Dict, List, Optional, Iterable, Generator

from libboutique.services.common.base_package_service import BasePackageService
from libboutique.common.transaction_feedback_decorator import transaction_feedback_decorator
from libboutique.common.transaction_actions import TransactionActionsEnum

import gi

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib


class PackageKitService(BasePackageService):
    """
        Service that takes care of:
        * Install a package
        * List installed packages
        * Uninstall a package
        * Search for a package

        ***********PACKAGE_FORMAT_EXPECTED**********
        ############################################
        ##### package_name;version;arch;distro #####
        ############################################
        ********************************************
    """

    PACKAGE_TYPE = "apt"

    def __init__(self, progress_publisher=None):
        super().__init__(progress_publisher=progress_publisher)
        self.packagekit_client = PackageKitGlib.Client().new()

    def _progress_callback(
        self,
        progress: PackageKitGlib.Progress,
        progress_type: PackageKitGlib.ProgressType,
        *user_data: Optional[object],
    ) -> None:
        """
        """
        if self.progress_publisher is None:
            return

    def list_installed_packages(self) -> List:
        """
            Takes care of retrieving and
            returning a list of installed packages
        """
        return self._create_dict_array_from_package_array(
            package_iterable=(
                p
                for p in self.packagekit_client.get_packages(
                    filters=PackageKitGlib.FilterEnum.from_string("INSTALLED"),
                    cancellable=None,
                    progress_callback=self._progress_callback,  # TODO Change for an internal callback
                    progress_user_data=(),  # TODO Change for user_data sent from outside
                ).get_package_array()
                if "installed" in p.get_data()
            )
        )

    @transaction_feedback_decorator(action=TransactionActionsEnum.REMOVE)
    def remove_package(self, name: str):
        """
            The name has to be formatted as a package_id
            ** see class pydoc **

            Transaction Flags Docs: http://tiny.cc/dynhbz
        """
        result = self.packagekit_client.remove_packages(
            transaction_flags=1,
            package_ids=[name],
            allow_deps=True,
            autoremove=False,
            cancellable=None,
            progress_callback=self._progress_callback,
            progress_user_data=(),
        )
        self._remove_install_date(package_name=name.replace("installed:", "").strip())
        return result

    @transaction_feedback_decorator(action=TransactionActionsEnum.REPAIR)
    def repair_dpkg(self):
        """
            apt install --fix-broken
        """
        self.packagekit_client.repair_system(
            transaction_flags=1, cancellable=None, progress_callback=self._progress_callback, progress_user_data=()
        )

    @transaction_feedback_decorator(action=TransactionActionsEnum.LIST_INSTALLED_REPOS)
    def list_installed_repos(self) -> Generator:
        """
            List the repos that are installed.
            Both the enabled and disabled are returned
        """
        repo_list = self.packagekit_client.get_repo_list(
            filters=1,  # Trusted
            cancellable=None,
            progress_callback=self._progress_callback,
            progress_user_data=()
        ).get_repo_detail_array()
        return (self._extract_repo_to_dict(repo) for repo in repo_list)

    @transaction_feedback_decorator(action=TransactionActionsEnum.INSTALL)
    def install_package(self, name: str):
        """
            The name has to be formatted as a package_id
            ** see class pydoc **
            Transaction Flags Docs: http://tiny.cc/dynhbz
        """
        install_result = self.packagekit_client.install_packages(
            transaction_flags=1,  # Trusted
            package_ids=[name],
            cancellable=None,
            progress_callback=self._progress_callback,
            progress_user_data=None,
        )
        self._save_installation_date(package_name=name)
        return install_result

    @transaction_feedback_decorator(action=TransactionActionsEnum.GET_CATEGORIES)
    def retrieve_package_categories(self):
        """
            Retrieve the categories from PackageKitGlib
        """
        return self.packagekit_client.get_categories(cancellable=None,
                                                     progress_callback=self._progress_callback,
                                                     progress_user_data=None)

    def retrieve_package_information_by_name(self, name: str) -> List:
        """
            Return everything from a name provided
        """
        package_list = self.packagekit_client.get_packages(
            filters=PackageKitGlib.FilterEnum.from_string("NONE"),
            cancellable=None,
            progress_callback=self._progress_callback,
            progress_user_data=(),
        ).get_package_array()
        return self._create_dict_array_from_package_array(
            package_iterable=(p for p in package_list if name in p.get_name())
        )

    @transaction_feedback_decorator(TransactionActionsEnum.REFRESH_CACHE)
    def refresh_cache(self, force=True):
        return self.packagekit_client.refresh_cache(
            force - force, cancellable=None, progress_callback=self._progress_callback, progress_user_data=()
        )

    def _create_dict_array_from_package_array(self, package_iterable: Iterable) -> List:
        """
            extract data from each Package provided
        """
        return [self._extract_package_to_dict(package=p) for p in package_iterable]

    def _extract_package_to_dict(self, package):
        """
            Use the formatter to return a dictionnary
            filled all the informations found in the Package object
        """
        return {
            **super()._extract_package_to_dict(package),
            "arch": package.get_arch(),
            "data": package.get_data(),
            "is_installed": "installed" in package.get_data(),
        }

    @staticmethod
    def _extract_repo_to_dict(repository) -> Dict:
        """
        """
        return {
            "id": repository.get_id(),
            "description": repository.get_description(),
            "enabled": repository.get_enabled(),
        }

    def _extract_information_from_strings(self, package):
        """__extract_information_from_strings
            Some Package informations are stored in
            strings or Enums. This function
            has for purpose to extract those embedded informations
        :doc: https://lazka.github.io/pgi-docs/#PackageKitGlib-1.0/classes/Package.html#PackageKitGlib.Package
        """
        # TODO Extract data from the Package Data
        pass
