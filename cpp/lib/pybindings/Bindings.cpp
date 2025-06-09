
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <sort/Sort.hpp>

namespace py = pybind11;

namespace {
template<typename Functor>
py::list sort_list(py::list& list, Functor sort) {
    const auto& element = list[0];
    if (py::isinstance<py::int_>(element)) {
        auto v = list.cast<std::vector<int>>();
        sort(v);
        return py::cast(v);
    }
    if (py::isinstance<py::float_>(element)) {
        auto v = list.cast<std::vector<float>>();
        sort(v);
        return py::cast(v);
    }
    if (py::isinstance<py::str>(element)) {
        auto v = list.cast<std::vector<std::string>>();
        sort(v);
        return py::cast(v);
    }

    throw std::runtime_error("Unsupported type.");
}
}

PYBIND11_MODULE(sorting_algorithms, module) {
    //// Heap sort
    module.def(
            "heap_sort",
            [](py::list& list) { return sort_list(list, [](auto& v) { algorithm::heap::sort(v); }); },
            "Sort a list using heap sort");

    //// Quick sort
    module.def(
            "quick_sort",
            [](py::list& list) { return sort_list(list, [](auto& v) { algorithm::quick::sort(v); }); },
            "Sort a list using quick sort");

    //// Insertion sort
    module.def(
            "insertion_sort",
            [](py::list& list) { return sort_list(list, [](auto& v) { algorithm::insertion::sort(v); }); },
            "Sort a list using insertion sort");

    //// Merge sort
    module.def(
            "merge_sort",
            [](py::list& list) { return sort_list(list, [](auto& v) { algorithm::merge::sort(v); }); },
            "Sort a list using merge sort");
}
