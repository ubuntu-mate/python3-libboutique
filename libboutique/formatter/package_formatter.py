class PackageFormatter():
    def __init__(self):
        pass

    @staticmethod
    def format_package_informations(name, dev, icon, summary, platform, source,
                                    package_type, dependencies, version,
                                    is_installed, version_installed, distro):
        """format_package_informations

        Information for the front-end - Those informations
        should be provided back to the backend so it can be
        installed.

        :param name: str
        :param dev: str
        :param icon: str
        :param summary: str
        :param platform: str
        :param source: str
        :param package_type: str
        :param dependencies: str
        :param version: str i.e 1.1.2-ubuntu
        :param is_installed: bool
        :param version_installed: str
        :param distro: str i.e ubuntu
        """
        return {
            "name": name,
            "dev_name": dev,
            "icon_path": icon,
            "summary": summary,
            "platform": platform,
            "source": source,
            "package_type": package_type,
            "dependencies": dependencies,
            "version": version,
            "is_installed": is_installed,
            "version_installed": version_installed,
            "distro": distro
        }
