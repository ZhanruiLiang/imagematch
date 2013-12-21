#pragma once

#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<exception>

class IPCSharedMemory {
public:
    class ShmGetException: public std::exception {};
    class ShmAttachException: public std::exception {};

    IPCSharedMemory(key_t key, size_t size):key(key), size(size) {
        if((shmid = shmget(key, size, 0666)) < 0 ) {
            throw ShmGetException();
        }
        if((buf = shmat(shmid, NULL, SHM_RDONLY)) == (void*)-1) {
            throw ShmAttachException();
        }
    }
    ~IPCSharedMemory() {
        shmdt(buf);
    }
    void * getBuffer()const { return buf; }
    key_t getKey()const { return key; }
    key_t getSize()const { return size; }
private:
    void * buf;
    int shmid;
    key_t key;
    size_t size;
};
