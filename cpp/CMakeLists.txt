cmake_minimum_required(VERSION 3.25)

project(sorting-algorithms CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(cmake/Compiler.cmake)
#include(cmake/Boost.cmake)
include(cmake/pybind11.cmake)

option(ENABLE_UNIT_TESTS "ENABLE UNIT TESTS" Off)

set(DIR_INCLUDE ${CMAKE_CURRENT_LIST_DIR}/include)
set(DIR_SOURCE ${CMAKE_CURRENT_LIST_DIR}/src)

add_subdirectory(lib/pybindings)

add_library(
    ${PROJECT_NAME}
        STATIC
        "${DIR_INCLUDE}/sort/Sort.hpp"
        "${DIR_SOURCE}/Sort.cpp"
)

target_include_directories(
        ${PROJECT_NAME}
        PUBLIC
            ${DIR_INCLUDE}
        PRIVATE
            ${DIR_SOURCE}
)

set_target_properties(
        ${PROJECT_NAME}
        PROPERTIES
            LINKER_LANGUAGE CXX
)

if(ENABLE_UNIT_TESTS)
    add_subdirectory(tests)
endif()