import pathlib
import os
import subprocess
from functools import lru_cache


class CuratedAppService:

	DIST_CURATED_APPS_FOLDER = "libboutique/curated_apps/dist"
	SCRIPT_CURATED_APPS_FOLDER = "libboutique/curated_apps/scripts"

	def build_index(self, *_, **__):
		command = ["sh", self._generate_path_to_build_index()]
		return subprocess.check_output(command, stderr=subprocess.PIPE)

	@lru_cache(maxsize=1)
	def _generate_path_to_build_index(self):
		return os.path.join(os.path.join(str(pathlib.Path.cwd()), self.SCRIPT_CURATED_APPS_FOLDER), "build.sh")


