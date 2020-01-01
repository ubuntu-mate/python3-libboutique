from libboutique.common import distro_wrapper
from libboutique.formatters.ppa_formatter import PPAFormatter


class TestPPAFormatter:

    USER = "graphics-team"
    PROJECT = "ppa"

    EXPECTED_LIST_FILENAME = f"graphics-team-ubuntu-ppa-{distro_wrapper.get_distro_codename()}.list"
    EXPECTED_FILE_PATH = f"/etc/apt/sources.list.d/graphics-team-ubuntu-ppa-{distro_wrapper.get_distro_codename()}.list"
    EXPECTED_REPOSITORY = "http://ppa.launchpad.net/graphics-team/ppa/ubuntu"

    def __enter__(self):
        return PPAFormatter(self.USER, self.PROJECT)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def test_format_list_filename(self):
        with self as ppa_formatter:
            list_filename = ppa_formatter.format_list_filename()
            assert self.EXPECTED_LIST_FILENAME == list_filename

    def test_format_file_path(self):
        with self as ppa_formatter:
            file_path = ppa_formatter.format_file_path()
            assert self.EXPECTED_FILE_PATH == file_path

    def test_format_repository(self):
        with self as ppa_formatter:
            repository = ppa_formatter.format_repository()
            assert repository == self.EXPECTED_REPOSITORY

    def test_format_file_content(self):
        with self as ppa_formatter:
            file_content = ppa_formatter.format_file_content()
            assert file_content == f"deb {self.EXPECTED_REPOSITORY} {distro_wrapper.get_distro_codename()} main"
