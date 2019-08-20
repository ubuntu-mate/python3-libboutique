from typing import List, Optional, Iterable

from libboutique.services.common.base_package_service import BasePackageService

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
    """

    def __init__(self, progress_publisher=None):
        super().__init__(progress_publisher=progress_publisher)
        self.package_type = "apt"
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
            returning a list of install packages
        """
        return self._create_dict_from_array(
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

    def install_package(self, name: str):
        # TODO Requires package_name;version;arch;distro as a string to install
        try:
            self.packagekit_client.install_package()
        except Exception as ex:
            print(ex)

    def _create_dict_from_array(self, package_iterable: Iterable) -> List:
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
            "source": package.get_data(),
            "version": package.get_version(),
            "is_installed": "installed" in package.get_data(),
        }

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
