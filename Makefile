# Adjust your python path here if needed
PYTHON := /usr/bin/python3

# sphinx-apidoc options
#  members : documents members functions
#  undoc-members : includes undocumented members in output
#  show-inheritance :
#  private-members : includes members starting with _
#  special-members : includes members like __foo__
#
SPHINX_APIDOC_OPTIONS := members,undoc-members,show-inheritance,private-members,special-members

NOSETESTS := nosetests

.PHONY: docs tests cov rtfm _devel _production devel dev production prod clean

default:
	@echo
	@echo "Available targets :"
	@echo
	@echo "       clean : cleans generated files, including doc"
	@echo "         cov : runs test suite with coverage"
	@echo "        docs : generates documentation"
	@echo "        rtfm : opens local documentation in browser"
	@echo "       tests : runs test suite"
	@echo
	@echo "Install targets :"
	@echo
	@echo " install.dev : installs developpment dependencies (system wide)"
	@echo "install.prod : installs production dependencies (system wide)"
	@echo " virtual.dev : installs developpment dependencies (in virtualenv)"
	@echo "virtual.prod : installs production dependencies (in virtualenv)"
	@echo

tests:
	#NOSE_DETAILED_ERRORS=1 NOSE_NOPATH=1 NOSE_VERBOSE=1 NOSE_PROCESSES=1 $(NOSETESTS)
	$(NOSETESTS) -d -v -P --processes=1
	#nosetests -d -v -P --processes=1

cov:
	#NOSE_WITH_COVERAGE=1 \
	#NOSE_COVER_PACKAGE=griotte \
	$(NOSETESTS) -d -v -P --with-coverage --cover-package=griotte --cover-html --cover-html-dir docs/_build/html/en/coverage/

bdist:
	$(PYTHON) setup.py bdist

sdist:
	$(PYTHON) setup.py sdist

doc docs:
	SPHINX_APIDOC_OPTIONS=$(SPHINX_APIDOC_OPTIONS) sphinx-apidoc -f -o docs/en/ griotte/lib/griotte/
	cd docs && make

rtfm:
	xdg-open docs/_build/html/en/index.html

_vdevel:
	$(PYTHON) devel-bootstrap.py -p $(PYTHON)

_vproduction:
	$(PYTHON) production-bootstrap.py -p $(PYTHON)

_devel:
	sudo pip install production-requirements.txt

_production:
	sudo pip install devel-requirements.txt

install.dev: _devel _production

install.prod: _production

virtual.dev: _vdevel _vproduction _vmessage

virtual.prod: _vproduction _vmessage

_vmessage:
	@echo "\n====================================\n"
	@echo "Please run :\n"
	@echo "source griotte/tools/env.sh"
	@echo

clean:
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*~" -or -name "#*" \) -delete
	find . -type f \( -name "*.swp" \) -delete
	find . -type d \( -name "__pycache__" \) -delete
	cd docs && make clean
	@rm -rf build/ dist/ pkg/
