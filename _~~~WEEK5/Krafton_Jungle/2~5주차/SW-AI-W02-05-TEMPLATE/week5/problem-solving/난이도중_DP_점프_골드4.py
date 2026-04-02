# DP - 점프 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/2253

n ,m = map(int, input().split())
block = []

for _ in range(m):
    block.append(int(input()))
INF = 10**9
max_jump = int((2 * n) ** 0.5) + 2

dp = [[INF] * (max_jump + 1) for _ in range(n+1)]
dp[1][0] = 0 

block = set(block)

for i in range(1, n+1):
    if i in block:
        continue

    for k in range(max_jump + 1):

        if dp[i][k] == INF:
         continue            

        for nk in [k-1, k, k+1]:
            if nk <= 0:
                continue

            ni = i + nk
            if ni > n or ni in block:
                continue

            dp[ni][nk] = min(dp[ni][nk], dp[i][k] + 1)


answer = min(dp[n])

if answer == INF:
    print(-1)
else:
    print(answer)
