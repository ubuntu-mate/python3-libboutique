class BasePackageService:

    def install_package(self, name):
        raise NotImplementedError("You must implement it in your class")

    def remove_package(self, name):
        raise NotImplementedError("You must implement it in your class")

    def retrieve_package_information_by_name(self, name):
        raise NotImplementedError("You must implement it in your class")

    def get_installed_package(self, name):
        raise NotImplementedError("You must implement it in your class")

    def _format_glib_error(self, exception):
        return {
            "args": exception.args,
            "code": exception.code,
            "domain": exception.domain,
            "message": exception.message
        }

    def _successful_message(self, action, package):
        return {
            "action": action,
            "name": package,
            "message": "success"
        }
