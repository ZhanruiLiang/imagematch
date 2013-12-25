all: _comparer.so

install: _comparer.so
	cp _comparer.so comparer.py ../../

comparer_wrap.cpp:
	swig -c++ -python -o comparer_wrap.cpp comparer.i

_comparer.so: comparer.cpp comparer_wrap.cpp
	g++ -O2 -shared -fPIC -std=c++11 \
		-I/usr/include/python2.7 \
		-I/usr/include/python2.7/config \
		comparer_wrap.cpp comparer.cpp \
		-o _comparer.so

test: _comparer.so
	python -c 'import comparer' 

clean:
	-rm _comparer.so comparer_wrap.cpp comparer.py
