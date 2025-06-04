
#include <boost/python.hpp>
#include <sort/Sort.hpp>

template<typename T>
void heap_sort(boost::python::list& container) {
}

template<typename T>
void quick_sort(boost::python::list& container) {
}

template<typename T>
void insertion_sort(boost::python::list& container) {
}

BOOST_PYTHON_MODULE(sorting_algorithms) {
    using namespace boost::python;
    //// Heapt sort
    def("heap_sort", heap_sort<int>);
    def("heap_sort", heap_sort<float>);
    def("heap_sort", heap_sort<std::string>);
    //// Quick sort
    def("quick_sort", quick_sort<int>);
    def("quick_sort", quick_sort<float>);
    def("quick_sort", quick_sort<std::string>);
    //// Insertion sort
    def("insertion_sort", insertion_sort<int>);
    def("insertion_sort", insertion_sort<float>);
    def("insertion_sort", insertion_sort<std::string>);
}

