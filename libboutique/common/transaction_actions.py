from enum import Enum


class TransactionActionsEnum(Enum):
    INSTALL = "install"
    REMOVE = "remove"
    SEARCH = "search"
    LIST_INSTALLED = "list_installed"
    LIST_INSTALLED_REPOS = "list_installed_repos"
    GET_CATEGORIES = "get_categories"
    REFRESH_CACHE = "refresh_cache"
    REPAIR = "dpkg_repair"
    ADD_PPA = "add_ppa"
    REMOVE_PPA = "remove_ppa"
