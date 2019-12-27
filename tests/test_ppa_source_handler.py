import os

from libboutique.ppa.source_handler import SourceHandler


class TestSourceHandler:

    def test_init_source_handler(self):
        source_handler = SourceHandler()
        assert source_handler.SOURCE_LIST_PATH == "/etc/apt/sources.list"
        assert source_handler.SOURCE_LIST_BACKUP_PATH == source_handler.SOURCE_LIST_PATH + ".back"

    def test_backup_source_list(self):
        source_handler = SourceHandler()
        if os.path.exists(source_handler.SOURCE_LIST_BACKUP_PATH):
            os.remove(source_handler.SOURCE_LIST_BACKUP_PATH)
        source_handler._backup_source_file()
        assert os.path.exists(source_handler.SOURCE_LIST_BACKUP_PATH)
        assert self._read_file_content(path=source_handler.SOURCE_LIST_PATH) == self._read_file_content(path=source_handler.SOURCE_LIST_BACKUP_PATH)

    @staticmethod
    def _read_file_content(path):
        with open(path, "r") as f:
            return f.readlines()