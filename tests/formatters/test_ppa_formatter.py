from libboutique.common import distro_wrapper
from libboutique.formatters.ppa_formatter import PPAFormatter


class TestPPAFormatter:

    USER = "graphics-team"
    PROJECT = "ppa"

    EXPECTED_LIST_FILENAME = f"graphics-team-ubuntu-ppa-{distro_wrapper.get_distro_codename()}.list"

    def test_format_list_filename(self):
        ppa_formatter = PPAFormatter(user=self.USER, project=self.PROJECT)
        list_filename = ppa_formatter.format_list_filename()
        assert self.EXPECTED_LIST_FILENAME == list_filename
