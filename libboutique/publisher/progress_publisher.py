from libboutique.metaclasses.singleton import Singleton


class ProgressPublisher(metaclass=Singleton):
    """ProgressPublisher"""

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, origin, callback):
        """subscribe

            subscribe with a string ( origin i.e console ) and
            a function that will receive the progression of the
            installation

        :param origin: console, webui ( str )
        :param callback: fn
        """
        self.subscribers.update({origin: callback})

    def unsubscribe(self, origin):
        """unsubscribe

        :param origin: string
        """
        self.subscribers.pop(origin)

    def publish(self, package, progress):
        """publish

            params stil TBD

        :param package:
        :param progress:  dict
        """
        for origin, callback in self.subscribers.items():
            callback(package, progress)
