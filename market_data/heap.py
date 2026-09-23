import pandas


class MinHeap:
    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.heap = []

    def insert(self, row: pandas.Series, gap_seconds: float):
        entry = (gap_seconds, row)

        if len(self.heap) < self.capacity:
            self.heap.append(entry)
            idx = len(self.heap) - 1
            while idx > 0:
                parent = (idx - 1) // 2
                if self.heap[parent][0] <= self.heap[idx][0]:
                    break
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            return

        if gap_seconds <= self.heap[0][0]:
            return

        self.heap[0] = entry
        idx = 0
        while 2 * idx + 1 < len(self.heap):
            child = 2 * idx + 1
            right = child + 1
            if right < len(self.heap) and self.heap[right][0] < self.heap[child][0]:
                child = right
            if self.heap[idx][0] <= self.heap[child][0]:
                break
            self.heap[idx], self.heap[child] = self.heap[child], self.heap[idx]
            idx = child
