cmake_minimum_required(VERSION 2.6)

add_definitions(
    -std=c++11
    -g
    # -O2
    -Wall
    )

add_executable(comparer src/comparer.cpp src/sharedmemory.hpp)
