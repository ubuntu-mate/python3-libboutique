import gi

from gi.repository import PackageKitGLib

from libboutique.services.common.base_package_service import BasePackageService

class PackageKitService(BasePackageService):

    def __init__(self, progress_publisher=None):
        self.packagekit_client = PackageKitGLib.Client().new()

    def progress_callback(self, client, change, deprecated, user_data):
    	pass

    def install_package(self, name):
    	pass

   	def remove_package(self, name):
   		pass

   	def get_installed_packages(self):
   		pass

   	def retrieve_package_information_by_name(self, name):
   		pass

   	def create_dict_from_array(self, package_array):
   		pass

   	def _extract_package_to_dict(self, package):
   		pass

