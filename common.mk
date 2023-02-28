LINTER = flake8
REQ_DIR = .
PYTESTFLAGS = -vv --verbose --tb=short --cov=$(PKG) --cov-branch --cov-report term-missing

FORCE:

prod: tests github

github: FORCE
	- git commit -a
	git push origin master

tests: lint unit

unit: FORCE
	pytest $(PYTESTFLAGS)

lint: FORCE
	$(LINTER) *.py

%.py: FORCE
	pytest -s tests/test_$*.py

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	make docs
