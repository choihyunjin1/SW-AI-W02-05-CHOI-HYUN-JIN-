# 그래프, DFS, BFS - 연결 요소의 개수 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/11724
from collections import deque
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

graph = [[] for _ in range(n+1)]
visited = [False] * (n+1)

for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

def bfs(start):
    queue = deque([start])
    visited[start] = True

    while queue:
        current = queue.popleft()
        for next_node in graph[current]:
            if not visited[next_node]:
                visited[next_node] = True
                queue.append(next_node)

count = 0

for i in range(1, n+1):
    if not visited[i]:
        bfs(i)
        count += 1

print(count)