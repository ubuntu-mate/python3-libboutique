import re

from typing import Tuple


class SourceHandler:
    """
        It takes care of the operations related to adding/removing
        external sources.

        This includes: ppa and custom urls
    """

    _REGEX_PPA = re.compile(r'^ppa:[a-z_-]+\/[a-z_-]+$')
    _PPA_STRING = "ppa:"
    _PPA_SEPARATOR = "/"

    def __init__(self):
        pass
    
    def _validate_ppa_format(self, uri: str) -> None:
        """
            Make sure the PPA uri is well formatted.

            ppa:user/project

        """
        if not self._REGEX_PPA.match(uri):
            raise RuntimeError("Invalid ppa uri")

    def _extract_information_from_ppa_uri(self, uri: str) -> Tuple:
        """
            Extract the user and the project from the 
            ppa URI

            1st -> User
            2nd -> Project
        """
        uri = uri[len(self._PPA_STRING):]
        information_array = uri.split(self._PPA_SEPARATOR)
        return tuple(information_array)

    def add_ppa_source(self, uri:str):
        self._validate_ppa_format(uri=uri)
        user. project = self._extract_information_from_ppa_uri(uri=uri)

