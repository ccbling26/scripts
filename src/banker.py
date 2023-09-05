import copy
from typing import List


class Banker:
    def __init__(self, available: List[int], max_required: List[List[int]]):
        self.m = len(available)
        self.n = len(max_required)

        self.available = available  # 可利用资源向量，每个元素代表每一类可利用资源的数目
        self.max_required = max_required  # 最大需求矩阵，n 个进程中的每一个进程对 m 类资源的最大需求
        self.allocations = [[0] * self.m for _ in range(self.n)]  # 分配矩阵，每个进程所持有的每类资源的数目
        self.need = max_required  # 每个进程尚需的每类资源数目

    def allocate(self, process_id: int, resource_id: int, count: int) -> bool:
        if count > self.need[process_id][resource_id]:
            # 超过进程所宣布的最大值
            return False
        elif count > self.available[resource_id]:
            # 没有足够的资源
            return False
        self.available[resource_id] -= count
        self.allocations[process_id][resource_id] += count
        self.need[process_id][resource_id] -= count
        if self._is_secure():
            return True
        else:
            self.available[resource_id] += count
            self.allocations[process_id][resource_id] -= count
            self.need[process_id][resource_id] += count
            return False

    def _is_secure(self):
        """在尝试分配完资源后，需要通过安全性算法，检测剩下的资源能不能让所有进程完成，如果不能则表示这次尝试分配不允许"""
        work = copy.deepcopy(self.available)
        finish = [False] * self.n
        i = 0
        while i < self.n:
            if finish[i]:
                i += 1
                continue
            flag = True
            for j in range(self.m):
                # 检测剩下的资源是否能够使进程 i 完成
                if self.need[i][j] > work[j]:
                    flag = False
                    break
            if flag:
                # 进程 i 可以完成，需要释放出其持有的资源
                finish[i] = True
                for j in range(self.m):
                    work[j] += self.allocations[i][j]
                i = 0
            else:
                i += 1
        for item in finish:
            if not item:
                return False
        return True
