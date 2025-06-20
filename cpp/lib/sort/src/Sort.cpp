
#include <sort/Sort.hpp>

#include <concepts>
#include <span>
#include <type_traits>
#include <vector>

namespace {

//// Heap sort

template<typename T>
void heapify(std::vector<T>& v, std::size_t n, std::size_t index) {
    auto largest = index;
    const auto left = 2 * index + 1;
    const auto right = 2 * index + 2;

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
    for (std::size_t i = low; i < high; ++i) {
        if (v[i] <= pivot) {
            std::swap(v[low], v[i]);
            ++low;
        }
    }
    std::swap(v[low], v[high]);
    return low;
}

template<typename T>
void quickSort(std::vector<T>& v, std::size_t low, std::size_t high) {
    if (low >= high || low > v.size() - 1 || high > v.size() - 1) {
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
concept TrivialType = std::is_trivially_copyable_v<T>;

template<typename T>
concept NonTrivialType = !TrivialType<T>;


template<NonTrivialType T>
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

template<TrivialType T>
void insertionSort(std::vector<T>& v) {
    if (v.empty()) {
        return;
    }

    for (std::size_t i = 1; i < v.size(); ++i) {
        const auto key = v[i];
        std::size_t j = i;

        while (j > 0 && v[j - 1] > key) {
            v[j] = std::move(v[j - 1]);
            --j;
        }
        v[j] = key;
    }
}

template<TrivialType T>
void merge(std::vector<T>& v, std::vector<T>& temp, std::size_t left, std::size_t mid, std::size_t right) {
    std::size_t i = left;
    std::size_t j = mid + 1;
    std::size_t k = left;

    while (i <= mid && j <= right) {
        if (v[i] <= v[j]) {
            temp[k++] = v[i++];
        } else {
            temp[k++] = v[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = v[i++];
    }

    while (j <= right) {
        temp[k++] = v[j++];
    }

    for (std::size_t index = left; index <= right; ++index) {
        v[index] = temp[index];
    }
}

template<NonTrivialType T>
void merge(std::vector<T>& v, std::vector<T>& temp, std::size_t left, std::size_t mid, std::size_t right) {
    std::size_t i = left;
    std::size_t j = mid + 1;
    std::size_t k = left;

    while (i <= mid && j <= right) {
        if (v[i] <= v[j]) {
            temp[k++] = std::move(v[i++]);
        } else {
            temp[k++] = std::move(v[j++]);
        }
    }

    while (i <= mid) {
        temp[k++] = std::move(v[i++]);
    }

    while (j <= right) {
        temp[k++] = std::move(v[j++]);
    }

    for (std::size_t l = left; l <= right; ++l) {
        v[l] = std::move(temp[l]);
    }
}

template<typename T>
void mergeSort(std::vector<T>& v, std::vector<T>& temp, std::size_t left, std::size_t right) {
    const auto size = v.size();
    if (left >= right || left > size - 1 || right > size - 1) {
        return;
    }

    const auto mid = (left + right) / 2;
    mergeSort(v, temp, left, mid);
    mergeSort(v, temp, mid + 1, right);
    merge(v, temp, left, mid, right);
}

template<typename T>
void mergeSort(std::vector<T>& v) {
    const auto size = v.size();
    if (v.empty() || v.size() <= 1) {
        return;
    }
    std::vector<T> temp(v);
    mergeSort(v, temp, 0, size - 1);
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

namespace merge {

void sort(std::vector<int>& container) {
    mergeSort(container);
}

void sort(std::vector<float>& container) {
    mergeSort(container);
}

void sort(std::vector<std::string>& container) {
    mergeSort(container);
}

}

} // namespace algorithm
