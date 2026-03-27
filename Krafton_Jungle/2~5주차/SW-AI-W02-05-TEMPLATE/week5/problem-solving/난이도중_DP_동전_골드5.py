# DP - 동전 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/9084

T = int(input())

for _ in range(T):
    n = int(input())
    coins = list(map(int, input().split()))
    m = int(input())

    dp = [0] * (m + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, m + 1):
            dp[i] += dp[i - coin]

    print(dp[m])

