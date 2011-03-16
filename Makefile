
DOCS         = docs
DOXYFILE     = docs/Doxyfile
DOXYDIR      = docs/doxygen

OUTPUT_DIST  = dist/
OUTPUT_BUILD = build/
PREFIX       = /usr/local
BINDIR       = /usr/local/bin

############  Rules  ############


all: $(wildcard $(OUTPUT_DIST)) $(wildcard $(OUTPUT_BUILD)) doxygen
	mkdir ./$(OUTPUT_BUILD)
	cp ./src/*.py  ./$(OUTPUT_BUILD)


check:
	echo "sorry, does not implement!"


clean:
	$(RM)  $(wildcard $(OUTPUT_DIST))
	$(RM) -r $(wildcard $(OUTPUT_BUILD))
	$(RM) -r $(wildcard $(DOXYDIR))


dist:
	echo "sorry, does not implement!"


install:
	cp -r ./$(OUTPUT_BUILD)/* $(PREFIX)/moldau/
	ln -s $(PREFIX)/moldau/moldau.py $(BINDIR)/moldau
	cp ./example/ $(PREFIX)/moldau/


uninstall:
	echo "sorry, does not implement!"


# build doxygen-docs
doxygen:
	doxygen $(DOXYFILE)

.PHONY: all check clean dist install uninstall doxygen
