import sys
from unittest.mock import Mock


class TestCommands:
	def test_rebuild_index_command(self):
		sys.argv[:-1] = ["--rebuild-index"]
		pass
