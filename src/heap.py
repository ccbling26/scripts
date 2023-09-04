from typing import List


class Heap:
    def __init__(self, arr: List[int]):
        self.arr = arr

    def _down(self, i: int, max_length: int):
        while True:
            c1 = 2 * (i + 1) - 1
            c2 = 2 * (i + 1)
            if c1 >= max_length:
                break
            elif c2 >= max_length or self.arr[c1] < self.arr[c2]:
                c = c1
            else:
                c = c2
            if self.arr[i] <= self.arr[c]:
                break
            self._swap(i, c)
            i = c

    def _swap(self, i: int, j: int):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def _up(self, i: int):
        while True:
            f = (i + 1) // 2 - 1
            if f < 0 or self.arr[f] <= self.arr[i]:
                break
            self._swap(f, i)
            i = f

    def heapify(self):
        """原地构建堆"""
        n = len(self.arr)
        for i in range(n // 2 - 1, -1, -1):
            self._down(i, n)

    def reverse(self):
        i, j = 0, len(self.arr) - 1
        while i < j:
            self._swap(i, j)
            i += 1
            j -= 1

    def sort(self, reverse: bool = False):
        n = len(self.arr) - 1
        while n >= 0:
            self._swap(0, n)
            n -= 1
            self._down(0, n + 1)
        if not reverse:
            self.reverse()


if __name__ == "__main__":
    arr = [8, 3, 5, 1, 6, 7, 0]
    h = Heap(arr)
    h.heapify()
    print(arr)
    h.sort()
    print(arr)
