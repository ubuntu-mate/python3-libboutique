import shutil
import re

from typing import Tuple


class SourceHandler:
    """
        It takes care of the operations related to adding/removing
        external sources.

        This includes: ppa and custom urls
    """
    LAUNCHPAD_URL = "http://ppa.launchpad.net/{user}/{project}/ubuntu"
    SOURCE_LIST_PATH = "/etc/apt/sources.list"
    SOURCE_LIST_BACKUP_PATH  = "/etc/apt/sources.list.back"

    _REGEX_PPA = re.compile(r'^ppa:[a-z_-]+\/[a-z_-]+$')
    _PPA_STRING = "ppa:"
    _PPA_SEPARATOR = "/"

    def __init__(self):
        pass
    
    def _backup_source_file(self) -> None:
        """
            Back the source.list file in case
            we need to do a rollback
        """
        shutil.copyfile(src=self.SOURCE_LIST_PATH, dst=self.SOURCE_LIST_BACKUP_PATH)

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