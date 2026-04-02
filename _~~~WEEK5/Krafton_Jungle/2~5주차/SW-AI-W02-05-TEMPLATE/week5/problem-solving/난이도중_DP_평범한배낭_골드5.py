# DP - 평범한 배낭 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/12865


n, k = map(int, input().split())
bag = []

for _ in range(n):
    bag.append(list(map(int, input().split())))

dp = [0] * (k + 1)

for w, v in bag:
    for j in range(k, w - 1, -1):
        dp[j] = max(dp[j], dp[j - w] + v)

print(dp[k])