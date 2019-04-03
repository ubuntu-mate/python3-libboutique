import unittest
import gi
from unittest.mock import Mock, patch

gi.require_version('Snapd', '1')
from gi.repository import Snapd
from gi.repository import GLib

from libboutique.services.snap.snap_service import SnapService


class TestSnapService(unittest.TestCase):
    """TestSnapService"""

    def validatePackageInformationDict(self, package):
        self.assertIsInstance(package, dict)
        self.assertNotEqual(package.get("id", None), None)
        self.assertNotEqual(package.get("name", None), None)
        self.assertEqual(package.get("type", None), "snap")
        self.assertNotEqual(package.get("revision", None), None)
        self.assertNotEqual(package.get("license", 1), 1)
        self.assertNotEqual(package.get("icon", 1), 1)
        self.assertNotEqual(package.get("download_size", None), None)
        self.assertNotEqual(package.get("install_date", 1), 1)

    def testInstallPackage(self):
        """testInstallPackage"""
        with patch.object(Snapd.Client, "new", return_value=Mock()) as snap_client_mock:
            publisher_mock = Mock()
            snap_service = SnapService(progress_publisher=publisher_mock)
            snap_client_mock.assert_called_once()
            snap_service.install_package(name="bw")
            snap_client = snap_service.snap_client
            snap_client.install2_sync.assert_called_once_with(flags=0,
                                                              name="bw",
                                                              channel="stable",
                                                              progress_callback=snap_service.progress_callback)

    def testRemovePackage(self):
        """testRemovePackage"""
        with patch.object(Snapd.Client, "new", return_value=Mock()) as snap_client_mock:
            publisher_mock = Mock()
            snap_service = SnapService(progress_publisher=publisher_mock)
            snap_client_mock.assert_called_once()
            snap_service.remove_package(name="bw")
            snap_client = snap_service.snap_client
            snap_client.remove_sync.assert_called_once_with(name="bw",
                                                            progress_callback=snap_service.progress_callback)

    def testInstallPackageTwice(self):
        """testInstallPackageTwice"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.install_package(name="bw")
        result = snap_service.install_package(name="bw")
        self.assertEqual(result.get("code"), 14)
        self.assertEqual(result.get("message"), 'snap "bw" is already installed')
        self.assertEqual(result.get("args"), ('snap "bw" is already installed',))
        self.assertEqual(result.get("domain"), "snapd-error-quark")

    def testInstallNewPackage(self):
        """testInstallNewPackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.install_package(name="bw")
        self.assertEqual(result.get("action"), "install")
        self.assertEqual(result.get("message"), "success")
        self.assertEqual(result.get("name"), "bw")

    def testRemoveTwicePackage(self):
        """testRemoveTwicePackage"""
        snap_service = SnapService(progress_publisher=None)
        snap_service.remove_package(name="bw")
        result = snap_service.remove_package(name="bw")
        self.assertEqual(result.get("code"), 15)
        self.assertEqual(result.get("message"), 'snap "bw" is not installed')
        self.assertEqual(result.get("args"), ('snap "bw" is not installed',))
        self.assertEqual(result.get("domain"), "snapd-error-quark")

    def testRetrieveInstalledPackage(self):
        snap_service = SnapService(progress_publisher=None)
        list_installed_packages = snap_service.get_installed_package()
        self.assertIsInstance(list_installed_packages, list)
        for package in list_installed_packages:
            self.validatePackageInformationDict(package=package)

    def testRetrieveInformationPackage(self):
        snap_service = SnapService(progress_publisher=None)
        package_info = snap_service.retrieve_package_information_by_name(name="bw")


if __name__ == "__main__":
    unittest.main()
