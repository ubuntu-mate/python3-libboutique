from libboutique.ppa.source_handler import SourceHandler

import pytest


class TestSourceHandler:

    valid_test_ppa = "ppa:graphics-drivers/ppa"

    valid_ppas = [
        "ppa:jflabonte/test",
        "ppa:graphics-drivers/ppa"
    ]

    invalid_ppas = [
        "jflable/test",
        "ppa:graphics-driver-ppa",
        "https://www.google.com",
        "ppa:graphics-drivers/ppa:jflabonte"
    ]

    @pytest.mark.parametrize("test_valid_ppas", valid_ppas)
    def test_validate_ppa_uri_valid(self, test_valid_ppas):
        source_handler = SourceHandler()
        source_handler._validate_ppa_format(uri=test_valid_ppas)

    @pytest.mark.parametrize("test_invalid_ppas", invalid_ppas)
    def test_validate_ppa_uri_invalid(self, test_invalid_ppas):
        source_handler = SourceHandler()
        with pytest.raises(RuntimeError):
            source_handler._validate_ppa_format(uri=test_invalid_ppas)

    def test_extract_ppa_information(self):
        source_handler = SourceHandler()
        user, project = source_handler._extract_information_from_ppa_uri(uri=self.valid_test_ppa)
        assert user == "graphics-drivers"
        assert project == "ppa"


    @staticmethod
    def _read_file_content(path):
        with open(path, "r") as f:
            return f.readlines()