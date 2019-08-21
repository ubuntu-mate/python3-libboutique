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
    def assert_package_structure(self, package):
        self.assertNotEqual(package.get('package_id'), None)
        self.assertNotEqual(package.get('name'), None)
        self.assertNotEqual(package.get('distribution'), None)
        self.assertNotEqual(package.get('version'), None)
        self.assertEqual(package.get('source'), "apt")
        self.assertNotEqual(package.get('summary'), None)
        self.assertNotEqual(package.get('arch'), None)
        self.assertNotEqual(package.get('data'), None)
        self.assertNotEqual(package.get('is_installed'), None)

    def test_list_installed_packages(self):
        install_packages = PackageKitService().list_installed_packages()
        for package in install_packages:
            self.assert_package_structure(package=package)
            self.assertEqual(package['is_installed'], True)
