#
# insertion sort
#

def insertion_sort(data):
    if not data:
        return
    
    for i in range(len(data)):
        key = data[i]
        j = i

        while j > 0 and data[j - 1] > key:
            data[j] = data[j - 1]
            j -= 1
        data[j] = key

#
# quick sort
#

def partition(data, low, high):
    pivot = data[high]
    i = low
    for j in range(low, high):
        if data[j] <= pivot:
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[high] = data[high], data[i]
    return i

def quick_sort(data):
    if not data:
        return
    _quick_sort(data, 0, len(data) - 1)


def _quick_sort(data, low, high):
    if low >= high or low > len(data) - 1 or high > len(data) - 1: 
        return
    
    pivot = partition(data, low, high)
    quick_sort(data, low, pivot - 1)
    quick_sort(data, pivot + 1, high)

# 
# heap sort
#

def heapify(data, n , index):
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < n and data[left] > data[largest]:
        largest = left

    if right < n and data[right] > data[largest]:
        largest = right

    if largest != index:
        data[index], data[largest] = data[largest], data[index]
        heapify(data, n, largest)                

def heap_sort(data):
    if not data:
        return
    
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[0], data[i] = data[i], data[0]
        heapify(data, i, 0)
