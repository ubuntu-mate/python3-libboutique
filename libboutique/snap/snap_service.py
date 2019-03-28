import gi
import os
import json

gi.require_version("Snapd", '1')
from gi.repository import Snapd

from libboutique.common.base_package_service import BasePackageService

class SnapService(BasePackageService):

    def __init__(self):
        self.snap_client = Snapd.Client().new()
        self.channel = "stable"
        self.package_type = "snap"

    def install_package(self, name):
        snap = self.snap_client.find_sync(flags=Snapd.FindFlags(1), query=name)
        return self.snap_client.install2_sync(flags=0, name=name, channel=self.channel)

    def remove_package(self, name):
        pass

    def retrieve_package_information_by_name(self, name):
        snap = self.snap_client.find_sync(query=name)
        return self._extract_snap_to_dict(snap=snap)

    def _extract_snap_to_dict(self, snap):
        return {
            "id": snap.get_id(),
            "name": snap.get_name(),
            "type": self.package_type,
            "revision": snap.get_revision(),
            "license": snap.get_license(),
            "icon": snap.get_icon(),
            "download_size": snap.get_download_size(),
            "install_date": snap.get_install_date()
        }

    def _build_install_args(self, name):
        """_build_install_args

            Build dictionnary that will passed as args using the ** operator

        :param name:
        """
        pass
