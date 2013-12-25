%module comparer

%{
#define SWIG_FILE_WITH_INIT
#include "comparer.hpp"
%}

%include "numpy.i"

%apply (float* IN_ARRAY1, int DIM1) {(float* buf1, int bufsize1), (float* buf2, int bufsize2)}

%inline %{
    double compare(
            int width1, int height1, float* buf1, int bufsize1, 
            int width2, int height2, float* buf2, int bufsize2
    ) {
        return 0.1;
        /*return _compareBuf(width1, height1, buf1, */
        /*        width2, height2, buf2);*/
    }
%}
