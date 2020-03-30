ACTIVATE := . venv/bin/activate &&
venv:
	@python3 -m venv venv
	$(ACTIVATE) pip3 install wheel
	@$(ACTIVATE) pip3 install -r requirements.txt

venv-test:
	@python3 -m venv venv
	@$(ACTIVATE) pip install -r requirements-test.txt

default: test

setup: develop

bdist bdist_wheel build develop install sdist: %:
	$(ACTIVATE) python setup.py $@

dist: venv build bdist bdist_wheel sdist

release: venv dist
	$(ACTIVATE) pip install twine
	$(ACTIVATE) python3 -m twine upload --repository-url=$(TWINE_REPOSITORY) dist/*

test: venv-test .tox
	$(ACTIVATE) tox

.tox: tox.ini
	@rm -rf .tox

clean:
	@find . -name \*~ -exec rm -v '{}' +
	@find . -name \*.pyc -exec rm -v '{}' +
	@find . -name __pycache__ -prune -exec rm -vfr '{}' +
	@rm -rf build bdist cover dist sdist
	@rm -rf .tox .eggs venv
	@find . \( -name \*.orig -o -name \*.bak -o -name \*.rej \) -exec rm -v '{}' +
	@rm -rf distribute-* *.egg *.egg-info *.tar.gz cover junit.xml coverage.xml .cache

.PHONY: default setup test clean