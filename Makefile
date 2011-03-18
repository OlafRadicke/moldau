
SHELL        = /bin/sh

DOCS         = ./docs
DOXYFILE     = ./docs/Doxyfile
DOXYDIR      = ./docs/doxygen

OUTPUT_DIST  = ./dist
OUTPUT_BUILD = ./build
PREFIX       = /usr/local/share
BINDIR       = /usr/local/bin

############  Rules  ############


all: $(wildcard $(OUTPUT_DIST)) $(wildcard $(OUTPUT_BUILD)) doxygen
	mkdir $(OUTPUT_BUILD)
	cp ./src/*.py  $(OUTPUT_BUILD)


check:
	echo "sorry, does not implement!"


clean:
	$(RM)  $(wildcard $(OUTPUT_DIST))
	$(RM) -r $(wildcard $(OUTPUT_BUILD))
	$(RM) -r $(wildcard $(DOXYDIR))


dist: doxygen
	mkdir $(OUTPUT_BUILD)
	cp ./GPL3.txt  $(OUTPUT_BUILD)
	cp ./README.txt  $(OUTPUT_BUILD)
	mkdir $(OUTPUT_BUILD)/src
	cp ./src/*.py  $(OUTPUT_BUILD)/src/
	mkdir ./$(OUTPUT_BUILD)/icons
	cp ./icons/*  $(OUTPUT_BUILD)/icons/
	cp -R ./example  $(OUTPUT_BUILD)
	mkdir $(OUTPUT_BUILD)/docs
	cp -R ./docs/*  $(OUTPUT_BUILD)/docs/
	ln -s $(OUTPUT_BUILD)/src/moldau.py $(OUTPUT_BUILD)/moldau

tar: dist
	tar -cvzf ./moldau_`date +%F`.tar.gz $(OUTPUT_BUILD)


install:
	cp -r $(OUTPUT_BUILD)/* $(PREFIX)/moldau/
	ln -s $(PREFIX)/moldau/moldau.py $(BINDIR)/moldau
	cp -R ./example $(PREFIX)/moldau/
	cp -R ./icons $(PREFIX)/moldau/


uninstall:
	$(RM) -r $(PREFIX)/moldau
	


# build doxygen-docs
doxygen:
	doxygen $(DOXYFILE)

.PHONY: all check clean dist install uninstall doxygen
