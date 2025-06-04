message(STATUS "Fetching PyBind11")

set(PYBIND_VERSION 2.13.6)
set(PYBIND_DESTINATION_DIR "${CMAKE_SOURCE_DIR}/external/pybind11/")
set(PYBIND_URL "https://github.com/pybind/pybind11/archive/refs/tags/v${PYBIND_VERSION}.tar.gz")

include(FetchContent)
set(FETCHCONTENT_QUIET FALSE)

FetchContent_Declare(
        pybind11
        URL ${PYBIND_URL}
        EXCLUDE_FROM_ALL
        SOURCE_DIR ${PYBIND_DESTINATION_DIR}
)

FetchContent_MakeAvailable(pybind11)

add_subdirectory(${PYBIND_DESTINATION_DIR})

if(POLICY CMP0167)
    cmake_policy(SET CMP0167 NEW)
endif()
