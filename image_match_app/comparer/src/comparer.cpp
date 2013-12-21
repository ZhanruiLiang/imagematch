#include "sharedmemory.hpp"
#include <cstdio>
#include <cstdlib>
#include <unordered_map>
#include <vector>

struct Color {
    unsigned char r, g, b;
};

const int BITS[3] = {6, 6, 6};
class ConvertedColor {
public:
    ConvertedColor() {}
    ConvertedColor(const Color& p) {
        r = p.r >> (8 - BITS[0]);
        g = p.g >> (8 - BITS[1]);
        b = p.b >> (8 - BITS[2]);
    }
    unsigned getKey()const {
        unsigned key = r;
        key = (key << BITS[0]) | g;
        key = (key << BITS[1]) | b;
        return key;
    }
private:
    unsigned char r, g, b;
};

class Image {
public:
    Image(const void * shmbuf) {
        width = ((unsigned long *)shmbuf)[0];
        height = ((unsigned long *)shmbuf)[1];
        Color* rawbuf = (Color *)((unsigned long *)shmbuf + 2);
        buf.resize(width * height);
        for(int i = 0; i < (int)buf.size(); i++) {
            buf[i] = ConvertedColor(rawbuf[i]);
        }
    }

    const ConvertedColor & getColorAt(int i) const {
        return buf[i];
    }

    int getSize() const { 
        return buf.size();
    }

private:
    unsigned long width, height;
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


double compare(const Image& img1, const Image& img2) {
    Histogram h1(img1), h2(img2);
    double rate = 0;
    // return rate;
    for(auto & kv: h1) {
        unsigned key = kv.first;
        if(h2.find(key) == h2.end()) 
            continue;
        rate += std::min(kv.second.p, h2[key].p);
    }
    return rate;
}

int main(int argc, char** argv) {
    if(argc < 5) {
        fprintf(stderr, "usage: comparer shmkey1 size1 shmkey2 size2\n");
        exit(1);
    }
    try {
        IPCSharedMemory 
            shm1(atoi(argv[1]), atoi(argv[2])),
            shm2(atoi(argv[3]), atoi(argv[4]));
        Image img1(shm1.getBuffer()), img2(shm2.getBuffer());
        double rate = compare(img1, img2);
        printf("%.6lf", rate);
        return 0;
    }catch(std::exception & ex) {
        fprintf(stderr, ex.what());
        return 1;
    }
}
