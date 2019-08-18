import gi
import unittest

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.packagekit.packagekit_service import PackageKitService


class TestPackageKitService(unittest.TestCase):
    """ def test_search_packages(self):
       package = "flat"
       package_kit_service = PackageKitService()
       result = package_kit_service.retrieve_package_information_by_name(name=package)
       for package in result:
           print(package)
           self.assertEqual(package, None)
    """

    def test_list_installed_packages(self):
        result = PackageKitService().list_installed_packages()
        for package in result:
            self.assertTrue("installed" in package.get_data())
