# test_sort.py

import unittest
import random
import string
from sort import insertion_sort, quick_sort, merge_sort, heap_sort

class TestSortingAlgorithms(unittest.TestCase):

    def setUp(self):
        self.n = 1000

    def generate_random_ints(self, n):
        return [random.randint(-1_000_000, 1_000_000) for _ in range(n)]

    def generate_random_floats(self, n):
        return [random.uniform(-1_000.0, 1_000.0) for _ in range(n)]

    def generate_random_strings(self, n, length=8):
        return [''.join(random.choices(string.ascii_letters, k=length)) for _ in range(n)]

    def run_sort_test(self, func, data):
        expected = sorted(data)
        result = func(data)
        self.assertEqual(data, expected)

    #
    # int tests
    #     

    def test_insertion_sort_ints(self):
        data = self.generate_random_ints(self.n)
        self.run_sort_test(insertion_sort, data)

    def test_quick_sort_ints(self):
        data = self.generate_random_ints(self.n)
        self.run_sort_test(quick_sort, data)

    def test_heap_sort_ints(self):
        data = self.generate_random_ints(self.n)
        self.run_sort_test(heap_sort, data)   

    def test_merge_sort_ints(self):
        data = self.generate_random_ints(self.n)
        self.run_sort_test(merge_sort, data)    

    #
    # float tests
    #

    def test_insertion_sort_floats(self):
        data = self.generate_random_floats(self.n)
        self.run_sort_test(insertion_sort, data)

    def test_quick_sort_floats(self):
        data = self.generate_random_floats(self.n)
        self.run_sort_test(quick_sort, data)

    def test_heap_sort_floats(self):
        data = self.generate_random_floats(self.n)
        self.run_sort_test(heap_sort, data)

    def test_merge_sort_floats(self):
        data = self.generate_random_floats(self.n)
        self.run_sort_test(merge_sort, data)    

    #
    # string test
    #

    def test_insertion_sort_strings(self):
        data = self.generate_random_strings(self.n)
        self.run_sort_test(insertion_sort, data)

    def test_quick_sort_strings(self):
        data = self.generate_random_strings(self.n)
        self.run_sort_test(quick_sort, data)
            
    def test_heap_sort_strings(self):
        data = self.generate_random_strings(self.n)
        self.run_sort_test(heap_sort, data)

    def test_merge_sort_strings(self):
        data = self.generate_random_strings(self.n)
        self.run_sort_test(merge_sort, data)    


if __name__ == "__main__":
    unittest.main()
