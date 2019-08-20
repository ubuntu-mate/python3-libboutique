import gi

from typing import Dict, List

gi.require_version("Snapd", "1")
from gi.repository import Snapd

from libboutique.services.common.base_package_service import BasePackageService


def _format_snap_version(snap):
    return "{version}-{revision}".format(version=snap.get_version(), revision=snap.get_revision())


class SnapService(BasePackageService):
    """
        Interface with PyObject Snapd.

        it takes care of :
        * install snaps
        * list installed snaps
        * remove a snap
        * help search for a snap using:
            * package name
    """

    def __init__(self, progress_publisher=None):
        super().__init__(progress_publisher=progress_publisher)
        self.snap_client = Snapd.Client().new()
        self._channel = "stable"
        self.package_type = "snap"

    def progress_callback(self, client: object, change: object, deprecated, user_data) -> None:
        """
            returns percent total and done
        """
        if self.progress_publisher is None:
            return
        total = 0
        done = 0
        for task in change.get_tasks():
            total += task.get_progress_total()
            done += task.get_progress_done()
        percent = round((done / total) * 100)
        self.progress_publisher.publish(client, {"percent": percent, "total": total, "done": done})

    def install_package(self, name: str) -> str:
        """
            Install a package providing it the name
            of the package you wish to install
        """
        try:
            if self.snap_client.install2_sync(
                flags=0, name=name, channel=self._channel, progress_callback=self.progress_callback
            ):
                return self._successful_message(action="install", package=name)
        except Exception as ex:
            return self._format_glib_error(exception=ex)

    def remove_package(self, name: str) -> str:
        """
            Remove a package using its name
        """
        try:
            if self.snap_client.remove_sync(name=name, progress_callback=self.progress_callback):
                return self._successful_message(action="remove", package=name)
        except Exception as ex:
            return self._format_glib_error(exception=ex)

    def list_installed_packages(self) -> List[Dict]:
        """
            List the packages that are installed on
            this machine
        """
        installed_snaps = self.snap_client.get_snaps_sync(flags=0, names=None)
        return self._create_array_dicts_from_array(snap_array=installed_snaps)

    def retrieve_package_information_by_name(self, name: str) -> List[Dict]:
        """
            Look for packages using  a name provided
        """
        snap = self.snap_client.find_sync(flags=Snapd.FindFlags(1), query=name)
        return self._create_array_dicts_from_array(snap[0])  # ( [ Snaps ], suggested_currency: )

    def _create_array_dicts_from_array(self, snap_array: List) -> List:
        """
            Extract information from the package
            in a normalized way
        """
        return [self._extract_package_to_dict(snap) for snap in snap_array]

    def _extract_package_to_dict(self, package) -> Dict:
        """
            Use Package Formatter to make sure
            all packages has the same object structure ( dict or json _
        """
        return {
            **super()._extract_package_to_dict(package=package),
            "dev_name": package.get_developer(),
            "icon": package.get_icon(),
            "license": package.get_license(),
            "version": _format_snap_version(snap=package),
            "installed_date": package.get_install_date(),
            "is_installed": True if package.get_install_date() is not None else False,
            "price": package.get_prices(),
        }
