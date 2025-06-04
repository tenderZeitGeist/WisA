project(pybindings)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

add_library(
        ${PROJECT_NAME}
        SHARED
        ${CMAKE_CURRENT_LIST_DIR}/Bindings.cpp
)

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
