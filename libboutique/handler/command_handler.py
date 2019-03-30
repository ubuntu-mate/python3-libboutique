from libboutique.metaclasses.singleton import Singleton
from libboutique.publisher.progress_publisher import ProgressPublisher
from libboutique.services.snap.snap_service import SnapService

class CommandHandler(metaclass=Singleton):
    """CommandHandler"""

    def __init__(self, origin, callback_subscribe):
        self.origin = origin
        self.callback_subscribe = callback_subscribe
        self.progress_publisher = ProgressPublisher()
        self.progress_publisher.subscribe(self.origin, self.callback_subscribe)
        self.snap_service = SnapService(progress_publisher=self.progress_publisher)

    def install_package(self, name):
        # TODO Curated package
        self.snap_service.install_package(name=name)
        # TODO APT

    def remove_package(self, name):
        # TODO Curated package
        self.snap_service.remove_package(name=name)
        # TODO APT

