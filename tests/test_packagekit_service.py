import gi

from typing import Dict

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.packagekit.packagekit_service import PackageKitService


class TestPackageKitService:
    """ def test_search_packages(self):
       package = "flat"
       package_kit_service = PackageKitService()
       result = package_kit_service.retrieve_package_information_by_name(name=package)
       for package in result:
           print(package)
           self.assertEqual(package, None)
    """

    def assert_package_structure(self, package: Dict) -> None:
        """
            Assert that the structure is as intended for now
        """
        assert package.get("package_id") is not None
        assert package.get("name") is not None
        assert package.get("distribution") is not None
        assert package.get("version") is not None
        assert package.get("source") == "apt"
        assert package.get("summary") is not None
        assert package.get("arch") is not None
        assert package.get("data") is not None
        assert package.get("is_installed") is not None

    def test_list_installed_packages(self):
        """
            Make sure that the result is a list of dict
            and that they are all tagged as installed
        """
        install_packages = PackageKitService().list_installed_packages()
        assert len(install_packages) >= 1000
        for package in install_packages:
            self.assert_package_structure(package=package)
            assert package["is_installed"]

