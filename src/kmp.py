class KMP:
    def __init__(self, pat: str):
        self.pat = pat
        self.m = len(pat)
        self.dp = [0] * self.m
        j = 0
        for i in range(1, self.m):
            while j > 0 and pat[i] != pat[j]:
                j = self.dp[j - 1]
            if pat[i] == pat[j]:
                j += 1
            self.dp[i] = j

    def search(self, txt: str):
        n = len(txt)
        j = 0
        for i in range(n):
            while j > 0 and txt[i] != self.pat[j]:
                j = self.dp[j - 1]
            if txt[i] == self.pat[j]:
                j += 1
            if j == self.m:
                return i - self.m + 1
        return -1


if __name__ == "__main__":
    txt = "aaacaaab"
    pat = "aaab"
    print(KMP(pat).search(txt))  # 4
