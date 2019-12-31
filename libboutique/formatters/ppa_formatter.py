from libboutique.common import distro_wrapper
from libboutique.templates import ppa_templates


class PPAFormatter:
    """
        Takes care of formatting strings
        that are required for handling ppas
    """

    def __init__(self, user: str, project: str):
        self.user = user
        self.project = project

    def format_list_filename(self) -> str:
        """
            i.e: user: graphics, project: ppa -> graphics-ubuntu-ppa-eoan.list
        """
        return f'{self.user}-{distro_wrapper.get_distro_id()}-{self.project}-{distro_wrapper.get_distro_codename()}.list'

    def format_file_path(self) -> str:
        """
            i.e: /etc/apt/sources.list.d/graphics-ubuntu-ppa-eoan.list
        """
        list_filename = self.format_list_filename(user=self.user, project=self.project)
        return ppa_templates.BASE_REPOSITORY_FILE_PATH.format(list_filename=list_filename)

    def format_repository(self) -> str:
        """
            i.e: http://ppa.launchpad.net/graphics/ppa/ubuntu
        """
        return ppa_templates.LAUNCHPAD_URL.format(user=self.user, project=self.project)

    def format_file_content(self):
        """
            i.e: deb http://ppa.launchpad.com/graphics/ppa/ubuntu eoan main
        """
        repository_url = self.format_repository()
        return ppa_templates.CONTENT_PPA_REPOSITORY_FILE.format(url=repository_url,
                                                                distro=distro_wrapper.get_distro_codename())
