import shutil
import re

from typing import Tuple

from libboutique.common import distro_wrapper


class SourceHandler:
    """
        It takes care of the operations related to adding/removing
        external sources.

        This includes: ppa and custom urls
    """
    PPA_CONFIG_TEMPLATE = "deb {url} {distro} main"

    LAUNCHPAD_URL = "http://ppa.launchpad.net/{user}/{project}/ubuntu"
    SOURCE_LIST_PATH = "/etc/apt/sources.list"
    SOURCE_LIST_BACKUP_PATH  = "/etc/apt/sources.list.back"
    NEW_PPA_BASE_PATH = "/etc/apt/sources.list.d/{package}"

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

    def _format__from_ppa(self, user: str, project: str) -> str:
        """

        """
        source_url = self.LAUNCHPAD_URL.format(user=user, project=project)
        return self.PPA_CONFIG_TEMPLATE.format(url=source_url, distro=distro_wrapper.get_distro_codename())

    def _format_ppa_file_path(self):
        return

    def add_ppa_source(self, uri:str):
        self._validate_ppa_format(uri=uri)
        user. project = self._extract_information_from_ppa_uri(uri=uri)

