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
        search_results = self.packagekit_client.search_details(filters=1, values=[name,], cancellable=None, progress_callback=self.progress_callback, progress_user_data=None)
        return self._create_dict_from_array(search_results.get_package_array())

    def _create_dict_from_array(self, package_array):
        packages = []
        for package in package_array:
            packages.append(self._extract_package_to_dict(package=package))
        return packages

    def _extract_package_to_dict(self, package):
        return PackageFormatter.format_package_informations(id_package=package.get_id(), name=package.get_name(),
         platform=package.get_arch(), summary=package.get_summary(), source="apt", package_type="apt", 
         version=package.get_version(), is_installed=package.get_data())
