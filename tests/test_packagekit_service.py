import gi

from typing import Dict
from time import time

from libboutique.services.packagekit.packagekit_service import PackageKitService
from libboutique.common.transaction_actions import TransactionActionsEnum
from tests.common_service_tests import CommonServiceTests

gi.require_version("PackageKitGlib", "1.0")
from gi.repository import PackageKitGlib


def retrieve_package_id_from_name(name):
    return PackageKitService().retrieve_package_information_by_name(name=name)[0].get("package_id")


GLANCES_PACKAGE = "glances"
FLASHBAKE_PACKAGE = "flashbake"


class TestPackageKitCommonService(CommonServiceTests):

    APPLICATION_TO_INSTALL_REMOVE = retrieve_package_id_from_name(name=GLANCES_PACKAGE)
    SECOND_APPLICATION_INSTALL_REMOVE = retrieve_package_id_from_name(name=FLASHBAKE_PACKAGE)
    PACKAGE_KIT_SERVICE = PackageKitService()

    PACKAGE_TYPE = "apt"

    def test_search_packages(self):
        package_name = "flat"
        result = self.PACKAGE_KIT_SERVICE.retrieve_package_information_by_name(name=package_name)
        assert len(result)
        for package in result:
            self.assert_package_structure(package=package)
            assert package_name in package.get("name")

    def test_install_a_package(self):
        result = self.PACKAGE_KIT_SERVICE.install_package(name=self.APPLICATION_TO_INSTALL_REMOVE)
        assert result.get("message") == "success"
        assert result.get("action") == "install"
        self.assert_installation_date(
            package_service=self.PACKAGE_KIT_SERVICE, expected_package_name=self.APPLICATION_TO_INSTALL_REMOVE
        )

    def test_remove_a_package(self):
        result = self.PACKAGE_KIT_SERVICE.remove_package(name=self.APPLICATION_TO_INSTALL_REMOVE)
        assert result.get("message") == "success"
        assert result.get("action") == "remove"
        self.assert_no_installation_date(
            package_service=self.PACKAGE_KIT_SERVICE, expected_package_name=self.APPLICATION_TO_INSTALL_REMOVE
        )

    def test_remove_uninstalled_package(self):
        package_kit_service = PackageKitService()
        result = package_kit_service.remove_package(name=self.APPLICATION_TO_INSTALL_REMOVE)
        assert result.get("message") == "success"
        assert result.get("action") == "remove"
        self.assert_no_installation_date(package_service=package_kit_service, expected_package_name=GLANCES_PACKAGE)

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

    def test_get_multiple_installation_dates(self):
        """
            Make that the installation dates are all in the database
        """
        pass

    def test_refresh_cache(self):
        """
            Test no force refresh cache
        """
        package_kit_service = PackageKitService()
        start_time = time()
        res = package_kit_service.refresh_cache()
        end_time = time()
        assert start_time < end_time
        self.assert_refresh_cache_structure(package_kit_service=package_kit_service, response=res)

    def test_force_refresh_cache(self):
        package_kit_service = PackageKitService()
        start_time = time()
        res = package_kit_service.refresh_cache()
        end_time = time()
        assert start_time < end_time
        time_elapsed = end_time - start_time
        assert time_elapsed > 2  # Determined that an apt update takes about 2 sec
        self.assert_refresh_cache_structure(package_kit_service=package_kit_service, response=res)

    def test_repair_dpkg(self):
        result = self.PACKAGE_KIT_SERVICE.repair_dpkg()
        assert result.get("action") == TransactionActionsEnum.REPAIR.value
        assert result.get("arguments") == ((self.PACKAGE_KIT_SERVICE,), {})
        assert result.get("message") == "success"

    def test_list_repos(self):
        result = self.PACKAGE_KIT_SERVICE.list_installed_repos()
        assert result.get("action") == TransactionActionsEnum.LIST_INSTALLED_REPOS.value
        assert result.get("arguments") == ((self.PACKAGE_KIT_SERVICE, ), {})
        list_results = result.get("result")
        assert isinstance(list_results, list)
        assert len(list_results) > 1
        for repo in list_results:
            assert isinstance(repo.get("description"), str)
            assert repo.get("enabled") is True

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

    @staticmethod
    def assert_refresh_cache_structure(package_kit_service, response):
        assert response.get("action") == TransactionActionsEnum.REFRESH_CACHE.value
        assert response.get("arguments") == ((package_kit_service,), {})
        assert response.get("message") == "success"
