# 백트래킹 - 외판원 순회 2 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/10971

import sys
input = sys.stdin.readline

N = int(input())
W = [list(map(int, input().split())) for _ in range(N)]

visited = [False] * N
answer = float('inf')

def dfs(start, now, count, cost):
    global answer

    # 현재 비용이 최소값보다 크면 넘김
    if cost >= answer:
        return

    # 모든 도시를 다 방문한 경우
    if count == N:
        # 현재 도시에서 시작 도시로 돌아갈 수 있어야 함
        if W[now][start] != 0:
            answer = min(answer, cost + W[now][start])
        return

    for next in range(N):
        # 이미 방문한 도시는 건너뜀
        if visited[next]:
            continue

        # 갈 수 없는 길이면 건너뜀
        if W[now][next] == 0:
            continue

        visited[next] = True
        dfs(start, next, count + 1, cost + W[now][next])
        visited[next] = False  # 백트래킹

# 시작 도시를 0으로 고정
visited[0] = True
dfs(0, 0, 1, 0)

print(answer)