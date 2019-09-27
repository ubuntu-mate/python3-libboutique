SHELL := /bin/bash

init:
	sudo apt install python3-gi python3-sqlalchemy gir1.2-snapd-1 zenity gir1.2-packagekitglib-1.0

format:
	black --config pyproject.toml *

setup_dev:
	python3 -m venv .venv
	make init
	source .venv/bin/activate && pip install -r requirements.txt

unittest:
	sudo su -c "source .venv/bin/activate && coverage run -m pytest -v"

report:
	coverage report
	coverage html
