ACTIVATE := . venv/bin/activate &&

venv:
	@python3 -m venv venv
	@$(ACTIVATE) pip3 install -r requirements.txt

release: venv dist
	$(ACTIVATE) pip install twine
	$(ACTIVATE) python3 -m twine upload --repository-url=$(TWINE_REPOSITORY) dist/*

test: venv .tox
	$(ACTIVATE) tox

.tox: tox.ini
	@rm -rf .tox

clean:
	@find . -name \*~ -exec rm -v '{}' +
	@find . -name \*.pyc -exec rm -v '{}' +
	@find . -name __pycache__ -prune -exec rm -vfr '{}' +
	@rm -rf build bdist cover dist sdist
	@rm -rf .tox .eggs
	@find . \( -name \*.orig -o -name \*.bak -o -name \*.rej \) -exec rm -v '{}' +
	@rm -rf distribute-* *.egg *.egg-info *.tar.gz cover junit.xml coverage.xml .cache

.PHONY: default setup test clean