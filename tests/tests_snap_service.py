import unittest
import gi
from unittest.mock import Mock, patch

gi.require_version("Snapd", "1")
from gi.repository import Snapd

from libboutique.services.snap.snap_service import SnapService


class TestSnapService(unittest.TestCase):
    """TestSnapService"""

    def validate_package_information_dict(self, package):
        self.assertIsInstance(package, dict)
        self.assertNotEqual(package.get("id", None), None)
        self.assertNotEqual(package.get("name", None), None)
        self.assertEqual(package.get("package_type", None), "snap")
        self.assertNotEqual(package.get("version", None), None)
        self.assertNotEqual(package.get("license", 1), 1)  # The value expected is None
        self.assertNotEqual(package.get("is_installed", None), None)
        self.assertNotEqual(package.get("installed_date", 1), 1)
        self.assertEqual(package.get("distro", None), "ubuntu")
        self.assertNotEqual(package.get("version_installed", 1), 1)
        self.assertNotEqual(package.get("platform", 1), 1)
        self.assertNotEqual(package.get("price", None), None)
        self.assertNotEqual(package.get("summary", None), None)

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
        self.assertEqual(result.get("code"), 14)
        self.assertEqual(result.get("message"), 'snap "bw" is already installed')
        self.assertEqual(result.get("args"), ('snap "bw" is already installed',))
        self.assertEqual(result.get("domain"), "snapd-error-quark")

    def test_install_new_package(self):
        """testInstallNewPackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.install_package(name="bw")
        self.assertEqual(result.get("action"), "install")
        self.assertEqual(result.get("message"), "success")
        self.assertEqual(result.get("name"), "bw")

    def test_remove_package_twice(self):
        """testRemoveTwicePackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.remove_package(name="bw")
        self.assertEqual(result.get("code"), 15)
        self.assertEqual(result.get("message"), 'snap "bw" is not installed')
        self.assertEqual(result.get("args"), ('snap "bw" is not installed',))
        self.assertEqual(result.get("domain"), "snapd-error-quark")

    def test_retrieve_installed_package(self):
        snap_service = SnapService(progress_publisher=None)
        list_installed_packages = snap_service.list_installed_packages()
        self.assertIsInstance(list_installed_packages, list)
        for package in list_installed_packages:
            self.validate_package_information_dict(package=package)

    def test_retrieve_package_information(self):
        snap_service = SnapService(progress_publisher=None)
        package_info = snap_service.retrieve_package_information_by_name(name="bw")
        for package in package_info:
            self.validate_package_information_dict(package=package)


if __name__ == "__main__":
    unittest.main()
