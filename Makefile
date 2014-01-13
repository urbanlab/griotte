# Adjust your python path here if needed
PYTHON 								:= /usr/bin/python3

# sphinx-apidoc options
#  members : documents members functions
#  undoc-members : includes undocumented members in output
#  show-inheritance :
#  private-members : includes members starting with _
#  special-members : includes members like __foo__
#
SPHINX_APIDOC_OPTIONS := members,undoc-members,show-inheritance,private-members,special-members

NOSETESTS 						:= nosetests

.PHONY: docs tests cov rtfm _devel _production devel dev production prod clean

default:
	@echo
	@echo "Available targets :"
	@echo
	@echo "           clean : cleans generated files, including doc"
	@echo "             cov : runs test suite with coverage"
	@echo "       dev,devel : installs developpment dependencies"
	@echo "            docs : generates documentation"
	@echo " prod,production : installs production dependencies"
	@echo "            rtfm : opens local documentation in browser"
	@echo "           tests : runs test suite"
	@echo

tests:
	$(NOSETESTS) -d -v -P

cov:
	$(NOSETESTS) -d -v -P --with-coverage --cover-package=raspeomix

doc docs:
	SPHINX_APIDOC_OPTIONS=$(SPHINX_APIDOC_OPTIONS) sphinx-apidoc -f -o docs/en/ griotte/lib/griotte/
	cd docs && make

rtfm:
	xdg-open docs/_build/html/en/index.html

_devel:
	$(PYTHON) devel-bootstrap.py -p $(PYTHON)

_production:
	$(PYTHON) production-bootstrap.py -p $(PYTHON)

devel dev: _devel _production _message

production prod: _production _message

_message:
	@echo -e "\n====================================\n"
	@echo -e "Please run :\n"
	@echo "source bin/activate"
	@echo 'export PYTHONPATH=${PWD}/griotte/lib:$$PYTHONPATH'
	@echo

clean:
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*~" -or -name "#*" \) -delete
	find . -type f \( -name "*.swp" \) -delete
	cd docs && make clean
