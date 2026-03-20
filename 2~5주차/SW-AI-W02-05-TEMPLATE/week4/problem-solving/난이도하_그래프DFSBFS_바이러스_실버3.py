# 그래프, DFS, BFS - 바이러스 (백준 실버3)
# 문제 링크: https://www.acmicpc.net/problem/2606
import sys
input = sys.stdin.readline




n = int(input())
m = int(input())

graph = [[] for _ in range(n+1)]
for i in range(m):
    a,b = map(int,input().split())

    graph[a].append(b)
    graph[b].append(a)

visited = [False]*(n+1)
visited[1] = True


def dfs(node):
    for next_node in graph[node]:
        if not visited[next_node]:
            visited[next_node] = True
            dfs(next_node)

dfs(1)

print(visited.count(True)-1)