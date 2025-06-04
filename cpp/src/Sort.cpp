
#include <sort/Sort.hpp>

namespace {

//// Heap sort

template<typename T>
void heapify(std::vector<T>& v, std::size_t n, std::size_t index) {
    auto largest = index;
    const auto left = 2 * index + 1;
    const auto right = 2 * largest + 2;

    if (left < n && v[left] > v[largest]) {
        largest = left;
    }

    if (right < n && v[right] > v[largest]) {
        largest = right;
    }

    if (largest != index) {
        std::swap(v[index], v[largest]);
        heapify(v, n, largest);
    }
}

template<typename T>
void heapSort(std::vector<T>& v) {
    if (v.empty()) {
        return;
    }

    const auto n = v.size();
    for (int64_t i = n / 2 - 1; i >= 0; --i) {
        heapify(v, n, static_cast<std::size_t>(i));
    }

    for (std::size_t i = n - 1; i > 0; --i) {
        std::swap(v[0], v[i]);
        heapify(v, i, 0);
    }
}

//// Quick sort

template<typename T>
std::size_t partition(std::vector<T>& v, std::size_t low, std::size_t high) {
    const auto& pivot = v[high];
    auto i = low;
    for (std::size_t j = low; j < high; ++j) {
        if (v[j] <= pivot) {
            std::swap(v[i], v[j]);
            ++i;
        }
    }
    std::swap(v[i], v[high]);
    return i;
}

template<typename T>
void quickSort(std::vector<T>& v, std::size_t low, std::size_t high) {
    if (low >= high || low > v.size() - 1) {
        return;
    }

    const auto pivot = partition(v, low, high);
    quickSort(v, low, pivot - 1);
    quickSort(v, pivot + 1, high);
}



template<typename T>
void quickSort(std::vector<T>& v) {
    if (v.empty()) {
        return;
    }

    quickSort(v, 0, v.size() - 1);
}

//// Insertion sort

template<typename T>
void insertionSort(std::vector<T>& v) {
    if (v.empty()) {
        return;
    }

    for (std::size_t i = 1; i < v.size(); ++i) {
        const auto key = std::move(v[i]);
        std::size_t j = i;

        while (j > 0 && v[j - 1] > key) {
            v[j] = std::move(v[j - 1]);
            --j;
        }
        v[j] = std::move(key);
    }
}

} // namespace

namespace algorithm {

namespace heap {

void sort(std::vector<int>& container) {
    heapSort(container);
}

void sort(std::vector<float>& container) {
    heapSort(container);
}

void sort(std::vector<std::string>& container) {
    heapSort(container);
}

} // namespace heap

namespace quick {

void sort(std::vector<int>& container) {
    quickSort(container);
}

void sort(std::vector<float>& container) {
    quickSort(container);
}

void sort(std::vector<std::string>& container) {
    quickSort(container);
}

}

namespace insertion {

void sort(std::vector<int>& container) {
    insertionSort(container);
}

void sort(std::vector<float>& container) {
    insertionSort(container);
}

void sort(std::vector<std::string>& container) {
    insertionSort(container);
}

}

} // namespace algorithm
