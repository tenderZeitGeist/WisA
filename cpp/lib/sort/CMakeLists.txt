project(sorting-algorithms CXX)

set(DIR_INCLUDE ${CMAKE_CURRENT_LIST_DIR}/include)
set(DIR_SOURCE ${CMAKE_CURRENT_LIST_DIR}/src)

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

