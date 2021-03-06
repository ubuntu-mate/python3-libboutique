from functools import partial
from threading import Thread
from typing import Callable, Tuple
from queue import Queue

from libboutique.metaclasses.singleton import Singleton
from libboutique.publisher.progress_publisher import ProgressPublisher
from libboutique.services.snap.snap_service import SnapService
from libboutique.services.packagekit.packagekit_service import PackageKitService


class PackageCommandHandler(metaclass=Singleton):
    """
        Takes care of the threads and process required
        to make the backend and frontend work seamlessly
    """

    _APT_QUEUE = Queue()
    _CURATED_QUEUE = Queue()
    _SNAP_QUEUE = Queue()

    _APT_DICT_KEY = "apt"
    _ACTION_QUEUE_DICT_KEY = "action_queue"
    _CURATED_DICT_KEY = "curated"
    _SERVICE_DICT_KEY = "service"
    _SNAP_DICT_KEY = "snap"
    _WORKER_DICT_KEY = "worker"

    def __init__(self, callback_subscribe, origin="console"):
        self._list_package_thread = Thread()
        self.callback_subscribe = callback_subscribe
        self.progress_publisher = ProgressPublisher()
        self.progress_publisher.subscribe(origin, self.callback_subscribe)
        self._package_type_services = {
            self._SNAP_DICT_KEY: {
                self._SERVICE_DICT_KEY: SnapService(progress_publisher=self.progress_publisher),
                self._ACTION_QUEUE_DICT_KEY: self._SNAP_QUEUE,
                self._WORKER_DICT_KEY: Thread(target=self._run_service_queue, args=(self._SNAP_QUEUE,)),
            },
            self._APT_DICT_KEY: {
                self._SERVICE_DICT_KEY: PackageKitService(progress_publisher=self.progress_publisher),
                self._ACTION_QUEUE_DICT_KEY: self._APT_QUEUE,
                self._WORKER_DICT_KEY: Thread(target=self._run_service_queue, args=(self._APT_QUEUE,)),
            }
        }

    def install_package(self, name: str, package_type: str, callback: Callable) -> None:
        """
            From the information in the front-end, initiate an installation
            of thee back
        """
        try:
            package_type_service = self._package_type_services[package_type]
            service_queue = self._package_type_services[package_type][self._ACTION_QUEUE_DICT_KEY]
            callback_partial = self._build_partial_function(
                fn=self._package_type_services[package_type][self._SERVICE_DICT_KEY].install_package,
                args=(name,),
                callback=callback,
            )
            service_queue.put_nowait(callback_partial)
            self._start_the_worker(worker=package_type_service[self._WORKER_DICT_KEY])
        except KeyError:
            callback("Error")  # TODO Error handling is to be defined

    def remove_package(self, name: str, package_type: str, callback: Callable) -> None:
        """
            Takes care of populating the queue for the package_type specified.
        """
        try:
            package_type_service = self._package_type_services[package_type]
            service_queue = package_type_service[self._ACTION_QUEUE_DICT_KEY]
            callback_patial = self._build_partial_function(
                fn=package_type_service[self._SERVICE_DICT_KEY].remove_package, args=(name,), callback=callback
            )
            service_queue.put_nowait(callback_patial)
            self._start_the_worker(worker=package_type_service[self._WORKER_DICT_KEY])
        except KeyError:
            callback("Error")  # TODO Error handling is to be defined

    def list_installed_packages(self, callback: Callable) -> None:
        """
            Run a thread that will list every installed packages

        :raise RuntimeWarning
        """
        if not self._list_package_thread.isAlive():
            self._list_package_thread = Thread(target=self._run_list_installed_packages, args=(callback,)).start()
        elif self._list_package_thread.isAlive():
            raise RuntimeWarning("List installed package is still running")

    def _build_partial_function(self, fn: Callable, args: Tuple, callback: Callable) -> Callable:
        """
            Create a partial which will allow us to run our function in a thread or store it
            in a queue
        """
        service_install_method = partial(fn, *args)
        return partial(callback, service_install_method)

    def _run_list_installed_packages(self, callback: Callable):
        """
            TODO Make each service run simultaneously
        """
        list_of_packages = {}
        # list_of_packages.update({self._CURATED_DICT_KEY: None})  # TODO Change None for implementation for curated
        list_of_packages.update(
            {
                self._SNAP_DICT_KEY: self._package_type_services[self._SNAP_DICT_KEY][
                    self._SERVICE_DICT_KEY
                ].list_installed_packages()
            }
        )
        list_of_packages.update(
            {
                self._APT_DICT_KEY: self._package_type_services[self._APT_DICT_KEY][
                    self._SERVICE_DICT_KEY
                ].list_installed_packages()
            }
        )
        callback(list_of_packages)

    @staticmethod
    def _start_the_worker(worker: Thread) -> None:
        """
            We want only 1 thread running per service
            at a time
        """
        if not worker.alive():
            worker.start()

    @staticmethod
    def _run_service_queue(service_queue: Queue):
        while not service_queue.empty():
            service_queue.get()()  # Calling the function stored ( Install or Remove )
