# Crappy Makefile for iso14443a-poller

static:
	gcc -o iso14443a-poller iso14443a-poller.c -lnfc -lusb -static

dynamic:
	gcc -o iso14443a-poller iso14443a-poller.c -lnfc

strip:
	strip iso14443a-poller

install: strip
	/usr/bin/install -c iso14443a-poller /usr/bin/iso14443a-poller
