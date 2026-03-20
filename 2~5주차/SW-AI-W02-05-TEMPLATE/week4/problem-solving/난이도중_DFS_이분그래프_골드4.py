# DFS - 이분 그래프 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/1707
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def dfs(x, color):
    visited[x] = color

    for next_node in graph[x]:
        if visited[next_node] == 0:   
            if not dfs(next_node, -color):
                return False
        else:
            if visited[next_node] == visited[x]: 
                return False

    return True

k = int(input())

for _ in range(k):
    v, e = map(int, input().split())
    graph = [[] for _ in range(v + 1)]
    visited = [0] * (v + 1)   

    for _ in range(e):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    is_bipartite = True

    for i in range(1, v + 1):
        if visited[i] == 0:
            if not dfs(i, 1):
                is_bipartite = False
                break

    if is_bipartite:
        print("YES")
    else:
        print("NO")