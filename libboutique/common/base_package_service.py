class BasePackageService():

    def __init__(self):
        pass

    def install_package(self, name):
        raise NotImplemented("You must implement it in your class")

    def remove_package(self, name):
        raise NotImplemented("You must implement it in your class")

    def retrieve_package_information_by_name(self, name):
        raise NotImplemented("You must implement it in your class")
