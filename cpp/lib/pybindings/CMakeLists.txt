project(pybindings)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

add_library(
        ${PROJECT_NAME}
        SHARED
            ${CMAKE_CURRENT_LIST_DIR}/Bindings.cpp
)

if (MSVC)
    target_link_directories(
        ${PROJECT_NAME}
        PRIVATE
            ${Python3_LIBRARY_DIRS}
    )
endif()

target_link_libraries(
        ${PROJECT_NAME}
            sorting-algorithms
            pybind11::pybind11
)

set_target_properties(
        ${PROJECT_NAME}
        PROPERTIES
        OUTPUT_NAME
            sorting_algorithms
)
