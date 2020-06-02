import pathlib
import os
import subprocess
import json
from functools import lru_cache


class CuratedAppService:

	DIST_CURATED_APPS_FOLDER = "libboutique/curated_apps/dist"
	SCRIPT_CURATED_APPS_FOLDER = "libboutique/curated_apps/scripts"
	CURATED_APPS_APPLICATION_INDEX = "libboutique/curated_apps/dist/applications-en.json"

	def __init__(self):
		self._curated_apps_json = None

	def build_index(self, *_, **__):
		if self._curated_apps_json is None:
			command = ["sh", self._generate_path_to_build_index()]
			if subprocess.check_output(command, stderr=subprocess.PIPE):
				with open(self.CURATED_APPS_APPLICATION_INDEX, "r") as f:
					self._curated_apps_json = json.load(f)

	@lru_cache(maxsize=1)
	def _generate_path_to_build_index(self):
		return os.path.join(os.path.join(str(pathlib.Path.cwd()), self.SCRIPT_CURATED_APPS_FOLDER), "build.sh")


