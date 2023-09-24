from typing import Any, Optional


class Node:
    key: str
    val: Any
    pre: Optional["Node"]
    nxt: Optional["Node"]

    def __init__(self, key: str, val: Any):
        self.key, self.val = key, val
        self.pre, self.nxt = None, None


class LRU:
    def __init__(self, cap: int):
        self.data = {}
        self.head, self.tail = Node("head", None), Node("tail", None)
        self.head.nxt = self.tail
        self.tail.pre = self.head
        self.cap = cap
        self.length = 0

    def get(self, key: str):
        if key not in self.data:
            return None
        node = self.data[key]
        node.pre.nxt = node.nxt
        node.nxt.pre = node.pre
        node.pre = self.tail.pre
        node.nxt = self.tail
        self.tail.pre.nxt = node
        self.tail.pre = node
        return node.val

    def set(self, key: str, val: Any):
        if key in self.data:
            self.get(key)
            self.data[key].val = val
            return
        if self.length == self.cap:
            self._del(self.head.nxt.key)
        self.length += 1
        node = Node(key, val)
        self.data[key] = node
        node.pre = self.tail.pre
        node.nxt = self.tail
        self.tail.pre.nxt = node
        self.tail.pre = node

    def _del(self, key: str):
        del self.data[key]
        self.length -= 1
        node = self.head.nxt
        node.nxt.pre = self.head
        self.head.nxt = node.nxt
        del node


if __name__ == "__main__":
    lru = LRU(2)

    print(lru.get("0"))  # None

    lru.set("1", 1)
    lru.set("2", 2)

    print(lru.get("1"))  # 1

    lru.set("3", 3)

    tmp = lru.head.nxt
    res = []
    while tmp != lru.tail:
        res.append(str(tmp.val))
        tmp = tmp.nxt

    print("->".join(res))  # 1->3
