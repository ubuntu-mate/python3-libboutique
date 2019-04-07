import unittest

from libboutique.services.packagekit.packagekit_service import PackageKitService

class TestPackageKitService(unittest.TestCase):

    def callback_ready(self, *args, **kwargs):
        print(args)
        print(kwargs)

    def test_search_packages(self):
        package = "flat"
        package_kit_service = PackageKitService()
        package_kit_service.retrieve_package_information_by_name(name=package, ready_callback=self.callback_ready)