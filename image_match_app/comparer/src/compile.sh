swig -c++ -python -o comparer_wrap.cpp comparer.i
g++ -O2 -shared -fPIC -std=c++11 \
    -o _comparer.so \
    -I/usr/include/python2.7 \
    -I/usr/include/python2.7/config \
    comparer_wrap.cpp comparer.cpp
# test
python2 -c 'import comparer'
