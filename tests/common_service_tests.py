from datetime import datetime

from libboutique.services.common.base_package_service import BasePackageService


class CommonServiceTests:
    PACKAGE_TYPE = "Unknown"

    def test_get_multiple_installation_dates(self):
        """
            Make that the installation dates are all in the database
        """
        raise NotImplemented

    @classmethod
    def assert_installation_date(cls, package_service: BasePackageService, expected_package_name: str) -> None:
        """
            Assert installation dates
        """
        installation_date = package_service.get_package_installation_date_by_package_name(package_name=expected_package_name)
        now = datetime.now()
        assert installation_date.package_type == cls.PACKAGE_TYPE
        assert installation_date.package_name == expected_package_name
        assert installation_date.installation_datetime.year == now.year
        assert installation_date.installation_datetime.month == now.month
        assert installation_date.installation_datetime.day == now.day
        assert installation_date.installation_datetime.hour == now.hour

    @classmethod
    def assert_no_installation_date(cls, package_service: BasePackageService, expected_package_name) -> None:
        """
            Assert that there is nothing in the database
        """
        assert package_service.get_package_installation_date_by_package_name(expected_package_name) is None

