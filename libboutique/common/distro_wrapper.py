from functools import lru_cache

from distro import LinuxDistribution


@lru_cache(maxsize=10)
def get_distro_codename() -> str:
    """
        Takes care of getting the distro.

        To reduce useless overhead, this function has the
        decorator @lru_cache
    """
    return LinuxDistribution.codename()
