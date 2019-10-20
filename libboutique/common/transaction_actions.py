from enum import Enum


class TransactionActionsEnum(Enum):
    INSTALL = "install"
    REMOVE = "remove"
    SEARCH = "search"
    LIST_INSTALLED = "list_installed"
    LIST_INSTALLED_REPOS = "list_installed_repos"
    REFRESH_CACHE = "refresh_cache"
    REPAIR = "dpkg_repair"
