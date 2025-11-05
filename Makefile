.PHONY: setup lint format type test cov docs release

setup:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev,docs,io]

lint:
	ruff check .

format:
	black .
	- toml-sort --in-place pyproject.toml
	- ruff format .
	- ruff check . --fix

type:
	mypy src

test:
	pytest

cov:
	pytest --cov=verbaterra --cov-report=term-missing --cov-fail-under=85
	- report-coverage

docs:
	mkdocs build

release:
	python -m pip install build
	python -m build
