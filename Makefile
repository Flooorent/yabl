.PHONY: tests

update_dep:
	pip-compile requirements.in
	pip-compile requirements-dev.in
	pip-sync requirements.txt requirements-dev.txt

run:
	export FLASK_APP=app.py; export FLASK_ENV=development; flask run

tests:
	pytest
