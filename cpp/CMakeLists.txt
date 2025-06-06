cmake_minimum_required(VERSION 3.25)

project(wisa-sorting-algorithms-cpp CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(cmake/Compiler.cmake)
#include(cmake/Boost.cmake)
include(cmake/pybind11.cmake)

option(ENABLE_UNIT_TESTS "ENABLE UNIT TESTS" Off)

add_subdirectory(lib/pybindings)
add_subdirectory(lib/sort)

if(ENABLE_UNIT_TESTS)
    add_subdirectory(tests)
endif()
