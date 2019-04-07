import gi

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.common.base_package_service import BasePackageService


class PackageKitService(BasePackageService):

    def __init__(self, progress_publisher=None):
      self.packagekit_client = PackageKitGlib.Client().new()
      self.progress_publisher = progress_publisher

    def progress_callback(self, client, change, deprecated, user_data):
        pass

    def callback_ready(self):
        pass

    def install_package(self, name):
        try:
            self.packagekit_client.install_package()
        except Exception as ex:
            print(ex)

    def remove_package(self, name):
        pass

    def get_installed_packages(self):
        pass

    def retrieve_package_information_by_name(self, name, ready_callback):
        client = self.packagekit_client.search_details_async(filters=1,
                                                             values=name,
                                                             cancellable=None,
                                                             progress_callback=self.progress_callback,
                                                             progress_user_data=None,
                                                             callback_ready=ready_callback,
                                                             user_data=None)

    def create_dict_from_array(self, package_array):
        pass

    def _extract_package_to_dict(self, package):
        pass

    def __create_package_id(self, name):
        pass