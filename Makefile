VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PYTEST := $(VENV_DIR)/bin/pytest

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

build:
	$(PYTHON) -m compileall src/

tests:
	$(PYTEST) test/

run:
	$(PYTHON) src/main.py

clean:
	rm -rf $(VENV_DIR)
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

