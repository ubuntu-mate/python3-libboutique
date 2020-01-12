SHELL := /bin/bash

init:
	sudo apt install python3-gi python3-sqlalchemy gir1.2-snapd-1 zenity gir1.2-packagekitglib-1.0 libcairo2-dev libgirepository1.0-dev -y

format:
	black --config pyproject.toml *

setup_dev:
	sudo pip3 install -r requirements.txt

unittest:
	sudo su -c "source .venv/bin/activate && coverage run -m pytest -v --maxfail=1 --log-file \"tests.log\""

report:
	coverage report
	coverage html

build_doc:
	cd docs && sphinx-build -b html source/ build/
