#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <unordered_map>
#include <vector>

#include "comparer.hpp"

struct Color {
    float l, a, b;
};

const int BITS[3] = {6, 6, 6};
const float MINS[3] = {0, -86.185, -107.863};
const float MAXS[3] = {100, 98.254, 94.482};


class ConvertedColor {
public:
    static unsigned char convert(float v, float min, float max, int bits) {
        return floor((v - min) / ((max - min) / (1 << bits))) + .5;
    }

    ConvertedColor() {}
    ConvertedColor(const Color& p) {
        l = convert(p.l, MINS[0], MAXS[0], BITS[0]);
        a = convert(p.l, MINS[1], MAXS[1], BITS[1]);
        b = convert(p.l, MINS[2], MAXS[2], BITS[2]);
    }
    unsigned getKey()const {
        unsigned key = l;
        key = (key << BITS[0]) | a;
        key = (key << BITS[1]) | b;
        return key;
    }
private:
    unsigned char l, a, b;
};

class Image {
public:
    Image(int width, int height, const float * fbuf):
            width(width), height(height){
        int size = width * height;
        buf.resize(size);
        for(int i = 0; i < size; i++) {
            buf[i] = ConvertedColor(Color{fbuf[i*3], fbuf[i*3+1], fbuf[i*3+2]});
        }
    }

    const ConvertedColor & getColorAt(int i) const {
        return buf[i];
    }

    int getSize() const { 
        return buf.size();
    }

private:
    int width, height;
    std::vector<ConvertedColor> buf;
};

struct Bin {
    ConvertedColor color;
    double p;
};

class Histogram: public std::unordered_map<unsigned, Bin> {
public:
    Histogram(const Image& image) {
        int n = image.getSize();
        for(int i = 0; i < n; i++) {
            const ConvertedColor& c = image.getColorAt(i);
            unsigned key = c.getKey();
            if(find(key) != end()) {
                (*this)[key].p += double(1.0) / n;
            }else{
                (*this)[key] = Bin{c, double(1.0)/n};
            }
        }
    }
};


double _compareImg(const Image& img1, const Image& img2) {
    Histogram h1(img1), h2(img2);
    double rate = 0;
    for(auto & kv: h1) {
        unsigned key = kv.first;
        if(h2.find(key) == h2.end()) 
            continue;
        rate += std::min(kv.second.p, h2[key].p);
    }
    return rate;
}

double _compareBuf(int width1, int height1, float* buf1,
        int width2, int height2, float* buf2) {
    return 0.1;
    // Image img1(width1, height1, buf1), img2(width2, height2, buf2);
    // return _compareImg(img1, img2);
}
