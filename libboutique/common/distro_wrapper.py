from functools import lru_cache

import distro


@lru_cache(maxsize=10)
def get_distro() -> str:
    """
        Takes care of getting the distro.

        To reduce useless overhead, this function has the
        decorator @lru_cache
    """
    return " ".join(distro.linux_distribution(full_distribution_name=False)[0:2])
