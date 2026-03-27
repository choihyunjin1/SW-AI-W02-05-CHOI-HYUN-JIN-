# 그리디 - 동전 0 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/11047


n ,k = map(int,input().split())
coins = []
for _ in range(n):
    coins.append(int(input()))
result = 0
coins.sort(reverse=True)

for i in range(len(coins)):
    cnt =k // coins[i]
    if cnt > 0:
        k = k%coins[i]
        result += cnt



print(result)