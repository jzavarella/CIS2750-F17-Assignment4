CC = gcc
CFLAGS = -Wall -std=c11 -g

CALENDARPARSERC = src/CalendarParser.c
CALENDARPARSERH = include/CalendarParser.h
CALENDARO = src/CalendarParser.o
CALENDARSO = bin/libcparse.so
APPBIN = APP/bin

LINKEDLISTC = src/LinkedListAPI.c
LINKEDLISTH = include/LinkedListAPI.h
LISTO = src/LinkedListAPI.o
LIBLIST = bin/libllist.a

INCLUDES = include/

all:
	make list
	make parserso

list: $(LINKEDLISTC) $(LINKEDLISTH)
	$(CC) $(CFLAGS) -fPIC -c $(LINKEDLISTC) -o $(LISTO) -I $(INCLUDES)
	ar cr $(LIBLIST) $(LISTO)

parserso: $(LINKEDLISTC) $(LINKEDLISTH) $(CALENDARPARSERC) $(CALENDARPARSERH)
	$(CC) $(CFLAGS) -fPIC -c $(CALENDARPARSERC) -o  $(CALENDARO) -I $(INCLUDES)
	$(CC) $(CFLAGS) $(CALENDARO) -Lbin/ -lllist -shared -o $(CALENDARSO)

run:
	python3 bin/A4main.py

clean:
	rm -f $(CALENDARSO) $(CALENDARO) $(LISTO) $(LIBLIST)
