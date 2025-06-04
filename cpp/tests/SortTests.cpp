
#include <gtest/gtest.h>

#include <algorithm>
#include <random>
#include <ranges>
#include <string>
#include <vector>

#include <sort/Sort.hpp>

namespace {

constexpr std::size_t kElements = 10000;

}

class SortingTestSuite : public ::testing::Test {
protected:
    void SetUp() override {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution intDistribution(0, 1000);
        std::uniform_real_distribution floatDistribution(0., 1000.);
        std::uniform_int_distribution charDistribution('a', 'z');

        m_ints.reserve(kElements);
        m_floats.reserve(kElements);
        m_strings.reserve(kElements);

        for (std::size_t i = 0; i < kElements; ++i) {
            m_ints.emplace_back(intDistribution(gen));
            m_floats.emplace_back(floatDistribution(gen));
            m_strings.emplace_back(10, charDistribution(gen));
        }
    }


    template<typename T, void (*Sort)(std::vector<T>&)>
    void checkSortingAlgorithm(std::vector<T>& v) {
        auto sortedData = v;
        std::ranges::sort(sortedData);
        Sort(v);
        ASSERT_EQ(v, sortedData);
    }

    template<typename T>
    void checkHeapSort(std::vector<T>& v) {
        checkSortingAlgorithm<T, algorithm::heap::sort>(v);
    }

    template<typename T>
    void checkQuickSort(std::vector<T>& v) {
        checkSortingAlgorithm<T, algorithm::quick::sort>(v);
    }

    template<typename T>
    void checkInsertionSort(std::vector<T>& v) {
        checkSortingAlgorithm<T, algorithm::insertion::sort>(v);
    }

    std::vector<int> m_ints;
    std::vector<float> m_floats;
    std::vector<std::string> m_strings;
};


class HeapSortTestSuite : public SortingTestSuite {
};

TEST_F(SortingTestSuite, heap_sort_integers) {
    checkHeapSort(m_ints);
}

TEST_F(SortingTestSuite, heap_sort_floats) {
    checkHeapSort(m_floats);
}

TEST_F(SortingTestSuite, heap_sort_strings) {
    checkHeapSort(m_strings);
}

TEST_F(SortingTestSuite, quick_sort_integers) {
    checkQuickSort(m_ints);
}

TEST_F(SortingTestSuite, quick_sort_floats) {
    checkQuickSort(m_floats);
}

TEST_F(SortingTestSuite, quick_sort_strings) {
    checkQuickSort(m_strings);
}

TEST_F(SortingTestSuite, insertion_sort_integers) {
    checkInsertionSort(m_ints);
}

TEST_F(SortingTestSuite, insertion_sort_floats) {
    checkInsertionSort(m_floats);
}

TEST_F(SortingTestSuite, insertion_sort_strings) {
    checkInsertionSort(m_strings);
}
