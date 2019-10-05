from functools import partial
from threading import Thread
from typing import Callable
from queue import Queue

from libboutique.metaclasses.singleton import Singleton
from libboutique.publisher.progress_publisher import ProgressPublisher
from libboutique.services.snap.snap_service import SnapService
from libboutique.services.packagekit.packagekit_service import PackageKitService


class PackageServicesController(metaclass=Singleton):
    """
        Takes care of the threads and process required
        to make the backend and frontend work seamlessly
    """

    _APT_QUEUE = Queue()
    _CURATED_QUEUE = Queue()
    _SNAP_QUEUE = Queue()

    _SERVICE_DICT_KEY = "service"

    def __init__(self, origin, callback_subscribe):
        self.origin = origin
        self.callback_subscribe = callback_subscribe
        self.progress_publisher = ProgressPublisher()
        self.progress_publisher.subscribe(self.origin, self.callback_subscribe)
        self._package_type_services = {
            "snap": {
                "service": SnapService(progress_publisher=self.progress_publisher),
                "action_queue": Queue()
            },
            "apt": {
                "service": PackageKitService(progress_publisher=self.progress_publisher),
                "action_queue": Queue()
            },
            "curated": {
                "service": None,  # TODO  replace None for the service intended for curated packages
                "action_queue": Queue()
            }
        }

    async def install_package(self, name, package_type: str, callback: Callable) -> None:
        """
            From the information in the front-end, initiate an installation
            of thee back
        """
        try:
            callback(self._package_type_services[package_type].install_package(name=name))
        except KeyError:
            callback("Error")  # TODO Error handling is to be defined

    def remove_package(self, name):
        # TODO Curated package
        self.snap_service.remove_package(name=name)
        # TODO APT

    def list_installed_packages(self):
        list_of_packages = {}
        list_of_packages.update({"curated": None})  # TODO Change None for implementation for curated
        list_of_packages.update({"snap": self.snap_service.list_installed_packages()})
        list_of_packages.update({"apt": None})  # TODO  Change None for implementation for apt
