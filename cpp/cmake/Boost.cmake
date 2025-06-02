message(STATUS "Fetching Boost")

set(BOOST_VERSION 1.88.0)
set(BOOST_ENABLE_CMAKE ON)

include(FetchContent)
set(FETCHCONTENT_QUIET FALSE)

FetchContent_Declare(
  Boost
        GIT_REPOSITORY https://github.com/boostorg/boost.git
        GIT_TAG boost-${BOOST_VERSION}
        GIT_SHALLOW TRUE
        GIT_PROGRESS TRUE
        OVERRIDE_FIND_PACKAGE TRUE
        EXCLUDE_FROM_ALL
)

find_package(
        Boost ${BOOST_VERSION} EXACT
        REQUIRED COMPONENTS python)

FetchContent_MakeAvailable(Boost)
