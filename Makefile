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

.PHONY: run-tests
run-tests:
	PYTHONPATH=. poetry run pytest --cov

.PHONY: run-workers-examples
run-workers-examples:
	@PYTHONPATH=. poetry run python ./examples/workers.py

.PHONY: run-llm-examples
run-llm-examples:
	@PYTHONPATH=. poetry run python ./examples/docstring_generator.py
