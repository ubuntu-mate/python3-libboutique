from datetime import datetime

from libboutique.database.models import InstallationDates


class CommonServiceTests:
    PACKAGE_TYPE = "Unknown"

    @classmethod
    def assert_installation_date(cls, installation_date: InstallationDates, expected_package_name: str) -> None:
        """
            Assert installation dates
        """
        assert installation_date.package_type == cls.PACKAGE_TYPE
        assert installation_date.package_name == expected_package_name
        assert installation_date.installation_datetime.year == datetime.now().year
        assert installation_date.installation_datetime.month == datetime.now().month
        assert installation_date.installation_datetime.day == datetime.now().day
        assert installation_date.installation_datetime.hour == datetime.now().hour
        assert installation_date.installation_datetime.minute == datetime.now().minute
