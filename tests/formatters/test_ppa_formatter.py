from libboutique.common import distro_wrapper
from libboutique.formatters.ppa_formatter import PPAFormatter


class TestPPAFormatter:

    USER = "graphics-team"
    PROJECT = "ppa"

    EXPECTED_LIST_FILENAME = f"graphics-team-ubuntu-ppa-{distro_wrapper.get_distro_codename()}.list"
    EXPECTED_FILE_PATH = f"/etc/apt/sources.list.d/graphics-team-ubuntu-ppa-{distro_wrapper.get_distro_codename()}.list"

    def __enter__(self):
        return PPAFormatter(self.USER, self.PROJECT)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def test_format_list_filename(self):
        ppa_formatter = PPAFormatter(user=self.USER, project=self.PROJECT)
        list_filename = ppa_formatter.format_list_filename()
        assert self.EXPECTED_LIST_FILENAME == list_filename

    def test_format_file_path(self):
        ppa_formatter = PPAFormatter(user=self.USER, project=self.PROJECT)
        file_path = ppa_formatter.format_file_path()
        assert self.EXPECTED_FILE_PATH == file_path
