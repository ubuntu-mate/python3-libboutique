init:
	sudo apt install gir1.2-snapd-1 zenity
	pip3 install -r requirements.txt

test:
	nosetests tests
