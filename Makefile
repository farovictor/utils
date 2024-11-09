.PHONY: install-python
install-python:
	pyenv install
	pyenv rehash

.PHONY: prepare-linters
prepare-linters:
	poetry run pre-commit install

.PHONY: run-linters
run-linters: prepare-linters
	poetry run pre-commit run -a
