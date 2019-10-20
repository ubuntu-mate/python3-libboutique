from enum import Enum


class TransactionActionsEnum(Enum):
    INSTALL = "install"
    REMOVE = "remove"
    SEARCH = "search"
    LIST_INSTALLED = "list"
    REFRESH_CACHE = "refresh_cache"
    REPAIR = "dpkg_repair"
