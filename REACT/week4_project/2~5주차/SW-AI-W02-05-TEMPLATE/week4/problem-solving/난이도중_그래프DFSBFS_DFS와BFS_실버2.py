# 그래프, DFS, BFS - DFS와 BFS (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/1260
from collections import deque

def bfs(graph, start):
    """
    너비 우선 탐색
    
    Args:
        graph: 그래프 딕셔너리
        start: 시작 정점
    
    Returns:
        방문 순서 리스트
    """
    visited = []
    
    # TODO: 큐 생성 및 시작 정점 추가
    ## 방문한 정점 집합
    pass
    deque([start])
    
    visited.append(start)

    queue = deque([start])

    while queue:
        current = queue.popleft()
    # TODO: 큐가 빌 때까지 반복
        deque(graph[current])
        for next_node in graph[current]:
    ## 큐에서 정점 꺼내기
    ## 인접한 정점들 확인
            if next_node not in visited:
                visited.append(next_node)
                queue.append(next_node)
    
    
    pass
    
    return visited


def dfs(graph, start, visited=None):
    """
    깊이 우선 탐색 (재귀)
    
    Args:
        graph: 그래프 딕셔너리
        start: 현재 정점
        visited: 방문 리스트
    
    Returns:
        방문 순서 리스트
    """
    # TODO: visited가 None이면 초기화
    pass
    if visited is None:
        visited = []
    # TODO: 현재 정점 방문
    pass
    visited.append(start)




    # TODO: 인접한 정점들에 대해 재귀
    ## 방문하지 않은 정점이면 재귀 호출
    for next_node in graph[start]:
        if next_node not in visited:
            dfs(graph, next_node, visited)
    pass
    
    return visited


n,m,v = map(int, input().split())
graph = [[] for _ in range(n+1)]
for _ in range(m):
    node1, node2 =  map(int, input().split())
    graph[node1].append(node2)
    graph[node2].append(node1)

for i in range(1, n+1):
    graph[i].sort()

print(*dfs(graph, v))
print(*bfs(graph, v))
