SHELL := /bin/bash

init:
	sudo apt install python3-venv python3-setuptools python3-gi python3-sqlalchemy gir1.2-snapd-1 zenity gir1.2-packagekitglib-1.0 libcairo2-dev libgirepository1.0-dev -y

format:
	black --config pyproject.toml *

create_dev_env:
	sudo python3 -m venv .venv

setup_dev:
	make create_dev_env && sudo su -c "source .venv/bin/activate && pip3 install -r requirements.txt"

unittest:
	sudo su -c "source .venv/bin/activate && coverage run -m pytest -v --maxfail=1 --log-file \"tests.log\""

report:
	coverage report
	coverage html

build_doc:
	cd docs && sphinx-build -b html source/ build/
