def add(num1: str, num2: str):
    f1, f2 = num1[0], num2[0]
    if f1 == "-" and f2 == "-":
        return "-" + _add(num1[1:], num2[1:])
    elif f1 != "-" and f2 != "-":
        return _add(num1, num2)
    if f1 == "-":
        if _cmp(num1[1:], num2) == num1[1:]:
            return "-" + _minus(num1[1:], num2)
        else:
            return _minus(num2, num1[1:])
    else:
        if _cmp(num1, num2[1:]) == num1:
            return _minus(num1, num2[1:])
        else:
            return "-" + _minus(num2[1:], num1)


def _add(num1: str, num2: str):
    added = 0
    i, j = len(num1) - 1, len(num2) - 1
    res = ""
    while i >= 0 and j >= 0:
        v1, v2 = 0, 0
        if i >= 0:
            v1 = int(num1[i])
            i -= 1
        if j >= 0:
            v2 = int(num2[j])
            j -= 1
        v = v1 + v2 + added
        added = v // 10
        res = str(v % 10) + res
    if added:
        res = "1" + res
    return res


def _cmp(num1: str, num2: str):
    n, m = len(num1), len(num2)
    if n > m:
        return num1
    elif n < m:
        return num2
    for i in range(n):
        if int(num1) > int(num2):
            return num1
        elif int(num1) < int(num2):
            return num2
    return num1


def _minus(num1: str, num2: str):
    borrow = 0
    i, j = len(num1) - 1, len(num2) - 1
    res = ""
    while i >= 0 and j >= 0:
        v1, v2 = 0, 0
        if i >= 0:
            v1 = int(num1[i])
            i -= 1
        if j >= 0:
            v2 = int(num2[j])
            j -= 1
        v = v1 - borrow - v2
        if v < 0:
            v += 10
            borrow = 1
        else:
            borrow = 0
        res = str(v) + res
    i = 0
    while i < len(res) and res[i] == "0":
        i += 1
    return res[i:] if i < len(res) else "0"
