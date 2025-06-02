
#include <sort/Sort.hpp>

namespace {

template <typename T>
void heapify(std::vector<T> &v, std::size_t n, std::size_t index) {
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

template <typename T>
void heapSort(std::vector<T> &v) {
  const auto n = v.size();
  for (int64_t i = n / 2 - 1; i >= 0; --i) {
    heapify(v, n, static_cast<std::size_t>(i));
  }

  for (std::size_t i = n - 1; i > 0; --i) {
    std::swap(v[0], v[i]);
    heapify(v, i, 0);
  }
}


template <typename T>
std::size_t partition(std::vector<T>& v, std::size_t low, std::size_t high) {
   return 0;
}

template <typename T>
void quickSort(std::vector<T>& v, std::size_t low, std::size_t high) {
  if (low >= high) {
    return;
  }

  const auto pivot = partition(v, low, high);
}

} // namespace

namespace algorithm {

namespace heap {

void sort(std::vector<int>& container) {
  heapSort(container);
}

void sort(std::vector<float> &container) {
  heapSort(container);
}

void sort(std::vector<std::string> &container) {
  heapSort(container);
}

} // namespace heap

} // namespace algorithm