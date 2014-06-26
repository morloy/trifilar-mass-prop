FILE="track.cpp"

all:
	g++ -ggdb `pkg-config --cflags opencv` -o `basename ${FILE} .cpp` ${FILE} `pkg-config --libs opencv`
