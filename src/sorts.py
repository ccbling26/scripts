import math
from typing import List

from src.heap import Heap


def check(arr: List[int]):
    """检查是否完成排序"""
    n = len(arr)
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            print("False")
            return
    print("True")


def bubble_sort(arr: List[int]):
    """冒泡排序"""
    n = len(arr)
    for i in range(n - 1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    check(arr)


def selection_sort(arr: List[int]):
    """选择排序"""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    check(arr)


def insertion_sort(arr: List[int]):
    """插入排序"""
    n = len(arr)
    for i in range(1, n):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break
    check(arr)


def shell_sort(arr: List[int]):
    """希尔排序"""
    n, gap = len(arr), 1
    while gap * 3 + 1 < n:
        gap = gap * 3 + 1
    while gap > 0:
        for i in range(gap, n):
            tmp = arr[i]
            j = i - gap
            while j >= 0 and arr[j] > tmp:
                arr[j + gap] = arr[j]
                j -= gap
            arr[j + gap] = tmp
        gap //= 3
    check(arr)


def merge_sort(arr: List[int]):
    """归并排序"""

    def sort(i: int, j: int):
        if i >= j:
            return
        elif i + 1 == j:
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
            return
        mid = (i + j) // 2
        sort(i, mid)
        sort(mid + 1, j)
        tmp = []
        a = i
        b = mid + 1
        while a <= mid and b <= j:
            if arr[a] < arr[b]:
                tmp.append(arr[a])
                a += 1
            else:
                tmp.append(arr[b])
                b += 1
        while a <= mid:
            tmp.append(arr[a])
            a += 1
        while b <= j:
            tmp.append(arr[b])
            b += 1
        for k in range(len(tmp)):
            arr[i + k] = tmp[k]

    sort(0, len(arr) - 1)
    check(arr)


def quick_sort(arr: List[int]):
    """快速排序"""

    def sort(i: int, j: int):
        if i >= j:
            return
        p, q = i, j
        while p < q:
            while p < q and arr[p] < arr[q]:
                p += 1
            if p < q:
                arr[p], arr[q] = arr[q], arr[p]
                q -= 1
            while p < q and arr[p] < arr[q]:
                q -= 1
            if p < q:
                arr[p], arr[q] = arr[q], arr[p]
                p += 1
        sort(i, p - 1)
        sort(p + 1, j)

    sort(0, len(arr) - 1)
    check(arr)


def heap_sort(arr: List[int]):
    """堆排序"""
    h = Heap(arr)
    h.heapify()
    h.sort()
    check(arr)


def count_sort(arr: List[int]):
    """计数排序"""
    min_val = arr[0]
    max_val = arr[0]
    for item in arr:
        if item < min_val:
            min_val = item
        if item > max_val:
            max_val = item
    tmp = [0] * (max_val - min_val + 1)
    for item in arr:
        tmp[item - min_val] += 1
    i = 0
    for j in range(len(tmp)):
        val = j + min_val
        for _ in range(tmp[j]):
            arr[i] = val
            i += 1
    check(arr)


def bucket_sort(arr: List[int]):
    """桶排序"""
    min_val = arr[0]
    max_val = arr[0]
    for item in arr:
        if item < min_val:
            min_val = item
        if item > max_val:
            max_val = item

    bucket_size = 5
    bucket_count = math.ceil((max_val - min_val + 1) / bucket_size)
    buckets = [[] for _ in range(bucket_count)]

    for item in arr:
        idx = math.ceil((item - min_val + 1) / bucket_size) - 1
        buckets[idx].append(item)
    for i in range(bucket_count):
        # 对每个桶排序，这里用到快速排序
        quick_sort(buckets[i])

    i = 0
    for j in range(bucket_count):
        for k in range(len(buckets[j])):
            arr[i] = buckets[j][k]
            i += 1

    check(arr)


def radix_sort(arr: List[int]):
    """基数排序"""
    base = 1
    tmp = [[] for _ in range(10)]
    while True:
        for item in arr:
            val = (item // base) % 10
            tmp[val].append(item)
        if len(tmp[0]) == len(arr):
            break
        arr = []
        for item in tmp:
            arr.extend(item)
        tmp = [[] for _ in range(10)]
        base *= 10
    check(arr)
