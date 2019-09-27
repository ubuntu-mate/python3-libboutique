from typing import Dict, List

from libboutique.database.models import db_session, InstallationDates

import distro

class BasePackageService:
    """
        Base class for each Package Services i.e PackageKit and Snap
    """
    PACKAGE_TYPE = "Unknown"

    def __init__(self, progress_publisher=None):
        self.distribution = " ".join(distro.linux_distribution(full_distribution_name=False)[0:2])
        self.progress_publisher = progress_publisher

    def install_package(self, name: str):
        raise NotImplementedError("You must implement it in your class")

    def remove_package(self, name: str):
        raise NotImplementedError("You must implement it in your class")

    def retrieve_package_information_by_name(self, name: str):
        raise NotImplementedError("You must implement it in your class")

    def list_installed_packages(self) -> List:
        raise NotImplementedError("You must implement it in your class")

    @staticmethod
    def get_all_package_installation_dates() -> [InstallationDates]:
        """
            Retrieve all the installation dates
        """
        with db_session() as session:
            return session.query(InstallationDates)

    @classmethod
    def get_package_installation_date_by_package_name(cls, package_name):
        with db_session() as session:
            return session.query(InstallationDates).filter(InstallationDates.package_name == package_name
                                                           and InstallationDates.package_type == cls.PACKAGE_TYPE).first()

    def _extract_package_to_dict(self, package) -> Dict:
        return {
            "package_id": package.get_id(),
            "name": package.get_name(),
            "distribution": self.distribution,
            "version": package.get_version(),
            "source": self.package_type,
            "summary": package.get_summary(),
        }

    def _save_installation_date(self, package_name):
        with db_session() as session:
            new_installation_date = InstallationDates(package_type=self.PACKAGE_TYPE, package_name=package_name)
            session.add(new_installation_date)

    @staticmethod
    def _remove_install_date(package_name):
        with db_session() as session:
            installation_date = session.query(InstallationDates).filter(InstallationDates.package_name == package_name)[0]
            session.delete(installation_date)
