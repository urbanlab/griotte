NOSETESTS := nosetests
PYTHON = /usr/bin/python3

.PHONY: docs

# tests:
# 	@for i in `ls test/test_*.py`; do \
# 		echo "$$i =>" ; \
# 		PYTHONPATH=".:lib" python $$i ; \
# 		echo ; \
# 	done

tests:
	$(NOSETESTS) -d -v -P

cov:
	$(NOSETESTS) -d -v -P --with-coverage --cover-package=raspeomix

docs:
	sphinx-apidoc -o docs/en/ src/lib/griotte/
	cd docs && make

rtfm:
	xdg-open docs/_build/html/en/index.html

_devel:
	$(PYTHON) devel-bootstrap.py -p /usr/bin/python3

production:
	$(PYTHON) production-bootstrap.py -p /usr/bin/python3

devel: _devel production

clean:
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*~" -or -name "#*" \) -delete
	find . -type f \( -name "*.swp" \) -delete
	cd docs && make clean
