message(STATUS "Fetching Boost")

set(BOOST_VERSION 1.88.0)
set(BOOST_DESTINATION_DIR "${CMAKE_SOURCE_DIR}/external/boost/")
set(BOOST_URL "https://github.com/boostorg/boost/releases/download/boost-${BOOST_VERSION}/boost-${BOOST_VERSION}-cmake.tar.gz")

include(FetchContent)
set(FETCHCONTENT_QUIET FALSE)

FetchContent_Declare(
        Boost
        URL ${BOOST_URL}
        EXCLUDE_FROM_ALL
        SOURCE_DIR ${BOOST_DESTINATION_DIR}
)

FetchContent_MakeAvailable(Boost)

if(POLICY CMP0167)
    cmake_policy(SET CMP0167 NEW)
endif()

find_package(
  Boost ${BOOST_VERSION} EXACT
  REQUIRED COMPONENTS python
)
