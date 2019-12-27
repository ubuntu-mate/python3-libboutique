from libboutique.ppa.source_handler import SourceHandler


class TestSourceHandler:

    def test_init_source_handler(self):
        source_handler = SourceHandler()
        assert source_handler.SOURCE_LIST_PATH == "/etc/apt/source.list"