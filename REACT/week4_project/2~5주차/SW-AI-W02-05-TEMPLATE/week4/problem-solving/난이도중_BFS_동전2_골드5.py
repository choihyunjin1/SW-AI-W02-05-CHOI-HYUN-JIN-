# BFS - 동전 2 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/2294


from collections import deque

n, k = map(int, input().split())

coins = []
for _ in range(n):
    coins.append(int(input()))

queue = deque()
queue.append((0, 0))

visited = [False] * (k + 1)
visited[0] = True

while queue:
    current, count = queue.popleft()

    for coin in coins:
        next_value = current + coin

        if next_value == k:
            print(count + 1)
            exit()

        if next_value < k and not visited[next_value]:
            visited[next_value] = True
            queue.append((next_value, count + 1))

print(-1)