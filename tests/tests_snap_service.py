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


if __name__ == "__main__":
    unittest.main()
