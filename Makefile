update-example:
	cookiecutter . --output-dir . --overwrite-if-exists

pyhipsterdev: update-example

test: pyhipsterdev
	cd pyhipsterdev && make shell

