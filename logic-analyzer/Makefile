all: edge towav

edge: edge.c
	cc -Wall -O2 -o edge edge.c

towav: towav.c
	cc -Wall -O2 -I /opt/homebrew/include -L /opt/homebrew/lib -o towav towav.c -lsndfile
