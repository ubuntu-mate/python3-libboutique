import gi

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.common.base_package_service import BasePackageService
from libboutique.formatter.package_formatter import PackageFormatter


class PackageKitService(BasePackageService):

    def __init__(self, progress_publisher=None):
      self.packagekit_client = PackageKitGlib.Client().new()
      self.progress_publisher = progress_publisher

    def progress_callback(self, status, typ, data=None):
        pass

    def callback_ready(self):
        pass

    def install_package(self, name):
        # TODO Requires package_name;version;arch;distro as a string to install
        try:
            self.packagekit_client.install_package()
        except Exception as ex:
            print(ex)

    def remove_package(self, name):
        pass

    def get_installed_packages(self):
        pass

    def retrieve_package_information_by_name(self, name):
        """retrieve_package_information_by_name

        Retrieve all available informations that can be taken
        from the package manager ( in our case apt) from a partial
        or complete name

        :param name: str
        :returns : list of dictionnaries with all the informations in the Package
        """
        search_results = self.packagekit_client.search_details(filters=1, values=[name,], cancellable=None, progress_callback=self.progress_callback, progress_user_data=None)
        return self._create_dict_from_array(search_results.get_package_array())

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

    def _extract_package_to_dict(self, package):
        """_extract_package_to_dict

        Use the formatter to return a dictionnary
        filled all the informations found in the Package object

        :param package: PackageKitGlib.Package
        :returns dict: Dictionnary of the information in the Package
        """
        return PackageFormatter.format_package_informations(id_package=package.get_id(), name=package.get_name(),
         platform=package.get_arch(), summary=package.get_summary(), source=package.get_data(), package_type="apt",
         version=package.get_version(), is_installed=package.get_data())

    def __extract_information_from_strings(self, package):
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

