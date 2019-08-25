import gi
from unittest.mock import Mock, patch

gi.require_version("Snapd", "1")
from gi.repository import Snapd

from libboutique.services.snap.snap_service import SnapService


class TestSnapService:
    """TestSnapService"""

    def validate_package_information_dict(self, package):
        assert isinstance(package, dict)
        assert package.get("package_id") is not None
        assert package.get("name") is not None
        assert package.get("source") == "snap"
        assert package.get("version") is not None
        assert package.get("license", 1) != 1  # Shouldn't be empty
        assert package.get("is_installed") is not None
        assert package.get("distribution") == "ubuntu 19.04"
        assert package.get("price") is not None
        assert package.get("summary") is not None

    def test_install_package(self):
        """testInstallPackage"""
        with patch.object(Snapd.Client, "new", return_value=Mock()) as snap_client_mock:
            publisher_mock = Mock()
            snap_service = SnapService(progress_publisher=publisher_mock)
            snap_client_mock.assert_called_once()
            snap_service.install_package(name="bw")
            snap_client = snap_service.snap_client
            snap_client.install2_sync.assert_called_once_with(
                flags=0, name="bw", channel="stable", progress_callback=snap_service.progress_callback
            )

    def test_remove_package(self):
        """testRemovePackage"""
        with patch.object(Snapd.Client, "new", return_value=Mock()) as snap_client_mock:
            publisher_mock = Mock()
            snap_service = SnapService(progress_publisher=publisher_mock)
            snap_client_mock.assert_called_once()
            snap_service.remove_package(name="bw")
            snap_client = snap_service.snap_client
            snap_client.remove_sync.assert_called_once_with(name="bw", progress_callback=snap_service.progress_callback)

    def test_install_package_twice(self):
        """testInstallPackageTwice"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.install_package(name="bw")
        result = snap_service.install_package(name="bw")
        assert result.get("code") == 14
        assert result.get("message") == 'snap "bw" is already installed'
        assert result.get("args") == ('snap "bw" is already installed',)
        assert result.get("domain") == "snapd-error-quark"

    def test_install_new_package(self):
        """testInstallNewPackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.install_package(name="bw")
        assert result.get("action") == "install"
        assert result.get("message") == "success"
        assert result.get("name") == "bw"

    def test_remove_package_twice(self):
        """testRemoveTwicePackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.remove_package(name="bw")
        assert result.get("code") == 15
        assert result.get("message") == 'snap "bw" is not installed'
        assert result.get("args") == ('snap "bw" is not installed',)
        assert result.get("domain") == "snapd-error-quark"

    def test_retrieve_installed_package(self):
        snap_service = SnapService(progress_publisher=None)
        list_installed_packages = snap_service.list_installed_packages()
        assert isinstance(list_installed_packages, list)
        for package in list_installed_packages:
            self.validate_package_information_dict(package=package)
            assert package.get("is_installed", False)

    def test_retrieve_package_information(self):
        snap_service = SnapService(progress_publisher=None)
        package_info = snap_service.retrieve_package_information_by_name(name="bw")
        for package in package_info:
            self.validate_package_information_dict(package=package)
