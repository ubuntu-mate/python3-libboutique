SHELL := /bin/bash

init:
	sudo apt install python3-gi gir1.2-snapd-1 zenity gir1.2-packagekitglib-1.0

setup_dev:
	python3 -m venv .venv
	make init
	source .venv/bin/activate && pip install -r requirements.txt

unittest:
	coverage run -m unittest discover tests -v
	coverage report
