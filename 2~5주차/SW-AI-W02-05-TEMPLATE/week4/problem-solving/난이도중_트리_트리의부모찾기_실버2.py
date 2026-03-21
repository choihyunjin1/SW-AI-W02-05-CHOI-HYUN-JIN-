# 트리 - 트리의 부모 찾기 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/11725
import sys
sys.setrecursionlimit(10**6) #<- 재귀 제한 해제
input = sys.stdin.readline #<- 읽기 최적화? 속도차이 9배

n = int(input())
graph = [[] for _ in range(n+1)]

parent = [0] * (n+1)

visited = [False]*(n+1)

for _ in range(n-1):
    node1, node2 = map(int,input().split())
    graph[node1].append(node2)
    graph[node2].append(node1)

def dfs(node):
    visited[node] =True




    for next_node in graph[node]:
        if not visited[next_node]:
            parent[next_node] = node
            dfs(next_node)

dfs(1)
for i in range(2,n+1):
    print(parent[i])