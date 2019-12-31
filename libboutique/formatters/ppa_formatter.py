from libboutique.common import distro_wrapper
from libboutique.templates import ppa_templates


def format_list_filename(user: str, project: str) -> str:
    """
        i.e: user: graphics, project: ppa -> graphics-ubuntu-ppa-eoan.list
    """
    return f'{user}-{distro_wrapper.get_distro_id()}-{project}-{distro_wrapper.get_distro_codename()}.list'


def format_file_path(user: str, project: str) -> str:
    """
        i.e: /etc/apt/sources.list.d/graphics-ubuntu-ppa-eoan.list
    """
    list_filename = format_list_filename(user=user, project=project)
    return ppa_templates.PPA_BASE_PATH.format(list_filename=list_filename)


def format_file_content(url):
    pass
