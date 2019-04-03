import unittest
import gi
from unittest.mock import Mock, patch

gi.require_version('Snapd', '1')
from gi.repository import Snapd

from libboutique.services.snap.snap_service import SnapService


class TestSnapService(unittest.TestCase):
    """TestSnapService"""

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
        snap_service = SnapService(progress_publisher=None)
        snap_service.install_package(name="bw")
        result = snap_service.install_package(name="bw")
        self.assertEqual(result.get("code"), 14)
        self.assertEqual(result.get("message"), 'snap "bw" is already installed')
        self.assertEqual(result.get("args"), ('snap "bw" is already installed',))
        self.assertEqual(result.get("domain"), "snapd-error-quark")


if __name__ == "__main__":
    unittest.main()
