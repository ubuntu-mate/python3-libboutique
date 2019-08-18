from typing import Callable, List, Optional

from libboutique.services.common.base_package_service import BasePackageService
from libboutique.formatter.package_formatter import PackageFormatter

import gi

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib


class PackageKitService(BasePackageService):
    """
    """

    def __init__(self, progress_publisher=None):
        self.packagekit_client = PackageKitGlib.Client().new()
        self.progress_publisher = progress_publisher

    def _progress_callback(
        self,
        progress: PackageKitGlib.Progress,
        progress_type: PackageKitGlib.ProgressType,
        *user_data: Optional[object]
    ) -> None:
        if self.progress_publisher is None:
            return

    def list_installed_packages(self) -> List:
        """
        """
        return [
            p
            for p in self.packagekit_client.get_packages(
                filters=PackageKitGlib.FilterEnum.from_string("INSTALLED"),
                cancellable=None,
                progress_callback=self._progress_callback,  # TODO Change for an internal callback
                progress_user_data=(),  # TODO Change for user_data sent from outside
            ).get_package_array()
            if "installed" in p.get_data()
        ]

    def install_package(self, name: str):
        # TODO Requires package_name;version;arch;distro as a string to install
        try:
            self.packagekit_client.install_package()
        except Exception as ex:
            print(ex)

    def _create_dict_from_array(self, package_array):
        """_create_dict_from_array
        extract data from each Package found
        :param package_array: [ PackageKitGlib.Package, ...]
        :returns : list of dictionnaries with all the informations in the Package
        """
        packages = []
        for package in package_array:
            packages.append(self._extract_package_to_dict(package=package))
        return packages

    @staticmethod
    def _extract_package_to_dict(package):
        """_extract_package_to_dict
        Use the formatter to return a dictionnary
        filled all the informations found in the Package object
        :param package: PackageKitGlib.Package
        :returns dict: Dictionnary of the information in the Package
        """
        return PackageFormatter.format_package_informations(
            id_package=package.get_id(),
            name=package.get_name(),
            platform=package.get_arch(),
            source=package.get_data(),
            package_type="apt",  # TODO Should in a variable ( find package manager )
            version=package.get_version(),
            is_installed=package.get_data(),
        )

    def _extract_information_from_strings(self, package):
        """__extract_information_from_strings
            Some Package informations are stored in
            strings or Enums. This function
            has for purpose to extract those embedded informations
        :doc: https://lazka.github.io/pgi-docs/#PackageKitGlib-1.0/classes/Package.html#PackageKitGlib.Package
        :param package:
        :return TBD -> TODO find out what can be extracted
        """
        # TODO Extract data from the Package Data
        pass
