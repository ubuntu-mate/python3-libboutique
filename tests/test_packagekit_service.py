import gi

from typing import Dict

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib

from libboutique.services.packagekit.packagekit_service import PackageKitService


class TestPackageKitService:

    APPLICATION_TO_INSTALL_REMOVE = "glances"

    @staticmethod
    def _retrieve_package_id_from_name(name):
        return PackageKitService().retrieve_package_information_by_name(name=name)[0].get("package_id")

    def test_search_packages(self):
        package_name = "flat"
        package_kit_service = PackageKitService()
        result = package_kit_service.retrieve_package_information_by_name(name=package_name)
        assert len(result)
        for package in result:
            self.assert_package_structure(package=package)
            assert package_name in package.get("name")

    def test_install_a_package(self):
        package_id = self._retrieve_package_id_from_name(name=self.APPLICATION_TO_INSTALL_REMOVE)
        package_kit_service = PackageKitService()
        result = package_kit_service.install_package(name=package_id)
        assert result.get("message") == "success"
        assert result.get("action") == "install"

    def test_remove_a_package(self):
        package_id = self._retrieve_package_id_from_name(name=self.APPLICATION_TO_INSTALL_REMOVE)
        package_kit_service = PackageKitService()
        result = package_kit_service.remove_package(name=package_id)
        assert result.get("message") == "success"
        assert result.get("action") == "remove"

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

    @staticmethod
    def assert_package_structure(package: Dict) -> None:
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
