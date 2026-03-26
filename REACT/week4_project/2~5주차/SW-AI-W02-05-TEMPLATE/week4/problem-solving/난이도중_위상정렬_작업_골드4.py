# 위상정렬 - 작업 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/2056

from collections import deque
import sys

input = sys.stdin.readline

n = int(input())

graph = [[] for _ in range(n + 1)]
indegree = [0] * (n + 1)
work_time = [0] * (n + 1)
finish_time = [0] * (n + 1)

for i in range(1, n + 1):
    data = list(map(int, input().split()))
    
    work_time[i] = data[0]
    cnt = data[1]
    
    for j in range(2, 2 + cnt):
        prev = data[j]
        graph[prev].append(i)
        indegree[i] += 1

queue = deque()

for i in range(1, n + 1):
    if indegree[i] == 0:
        queue.append(i)
        finish_time[i] = work_time[i]

while queue:
    now = queue.popleft()

    for next_node in graph[now]:
        if finish_time[next_node] < finish_time[now] + work_time[next_node]:
            finish_time[next_node] = finish_time[now] + work_time[next_node]

        indegree[next_node] -= 1

        if indegree[next_node] == 0:
            queue.append(next_node)

print(max(finish_time))