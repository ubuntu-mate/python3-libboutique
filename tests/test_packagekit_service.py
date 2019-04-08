import gi
import unittest

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.packagekit.packagekit_service import PackageKitService

class TestPackageKitService(unittest.TestCase):

    def test_search_packages(self):
        package = "flat"
        package_kit_service = PackageKitService()
        result = package_kit_service.retrieve_package_information_by_name(name=package)
        self.assertIsInstance(result, PackageKitGlib.Results)
        package_array = result.get_package_array()
        for package in package_array:
            self.assertEqual(package, PackageKitGlib.Package)