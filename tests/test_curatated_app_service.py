import os
from contextlib import contextmanager

from libboutique.services.curated_app_service import CuratedAppService


class TestCuratedAppService:

	@contextmanager
	def create_instance(self):
		curated_app_service = CuratedAppService()
		try:
			yield curated_app_service
		finally:
			del curated_app_service

	def read_file_content(self, path:str):
		with open(path, "r") as f:
			return f.read()

	def get_time_touched_fs(self, path: str) -> int:
		try:
			return os.stat(path).st_mtime
		except FileNotFoundError:
			return 0

	# def test_build_index(self):
	# 	with self.create_instance() as curated_app:
	# 		output = curated_app.build_index()
	# 		assert output is not None
	# 		assert isinstance(output, dict)
	# 		assert self.get_time_touched_fs(path=curated_app.DIST_CURATED_APPS_FOLDER)

