SHELL := /bin/bash

setup:
	sudo apt install python3-venv python3-setuptools python3-gi python3-pytest python3-flake8 python3-distro python3-sqlalchemy gir1.2-snapd-1 zenity gir1.2-packagekitglib-1.0 libcairo2-dev libgirepository1.0-dev -y
	git pull --recurse-submodules --update

format:
	black --config pyproject.toml *

unittest:
	sudo python3 -m pytest -v --maxfail=1 --log-file "tests.log"

report:
	coverage report
	coverage html

build_doc:
	cd docs && sphinx-build -b html source/ build/
