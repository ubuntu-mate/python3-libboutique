init:
	sudo apt install gir1.2-snapd-1 zenity python3-nose

setup_dev:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

test:
	coverage python setup.py test
	coverage report xml
