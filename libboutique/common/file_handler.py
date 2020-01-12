import os

def write_file(file_path: str, file_content: str, file_mode="w+") -> None:
    """
        Write a line or a preformated str to a file

        :param file_path: i.e /etc/apt/sources.list.d/ppa-graphic.conf
        :param file_content:
        :raises IOError
    """
    with open(file_path, file_mode) as f:
        f.write(file_content)


def file_exists(path:str) -> bool:
    """
        Simply return if the path provided exists

        Avoid to repeat ourselves or to import libraries everywhere
    """
    return os._exists(name=path)


def remove_file(file_path: str):
    """
        Remove a file
    """
    os.remove(path=file_path)
