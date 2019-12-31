from libboutique.common import distro_wrapper
from libboutique.templates import ppa_templates


def format_list_file(user: str, project: str) -> str:
    return f'{user}-{distro_wrapper.get_distro_id()}-{project}-{distro_wrapper.get_distro_codename()}.list'


def format_file_path(user, project):
    return ppa_templates.PPA_BASE_PATH.format(package=format_list_file(**locals()))


def format_file_content(url):
    pass
