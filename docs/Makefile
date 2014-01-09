# MakeFile for building all the docs at once.
# Inspired by the Makefile used by bazaar.
# http://bazaar.launchpad.net/~bzr-pqm/bzr/2.3/

PYTHON = python

.PHONY: all clean html latexpdf epub htmlhelp

# Dependencies to perform before running other builds.
# SPHINX_DEPENDENCIES =

# Make the HTML version of the documentation with correctly nested language folders.
html: $(SPHINX_DEPENDENCIES)
		cd en && make html LANG=en
		#cd fr && make html LANG=fr

htmlhelp: $(SPHINX_DEPENDENCIES)
		cd en && make htmlhelp LANG=en
		#cd fr && make htmlhelp LANG=fr

epub: $(SPHINX_DEPENDENCIES)
		cd en && make epub LANG=en
		#cd fr && make epub LANG=fr

latexpdf: $(SPHINX_DEPENDENCIES)
		cd en && make latexpdf LANG=en
		#cd fr && make latexpdf LANG=fr

clean:
		rm -rf _build/*

