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

	def test_build_index(self):
		with self.create_instance() as curated_app:
			curated_app.rebuild_index()

