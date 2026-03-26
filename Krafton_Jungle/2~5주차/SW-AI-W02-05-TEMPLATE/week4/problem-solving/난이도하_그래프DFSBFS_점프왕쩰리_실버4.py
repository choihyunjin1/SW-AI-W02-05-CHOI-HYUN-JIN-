# 그래프, DFS, BFS - 점프왕 쩰리 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/16173
def dfs(r, c, visited):
    if board[r][c] == -1:
        return True

    visited[r][c] = True
    jump = board[r][c]

    if r + jump < n and not visited[r + jump][c]:
        if dfs(r + jump, c, visited):
            return True

    if c + jump < n and not visited[r][c + jump]:
        if dfs(r, c + jump, visited):
            return True

    return False


n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]
visited = [[False] * n for _ in range(n)]

if dfs(0, 0, visited):
    print("HaruHaru")
else:
    print("Hing")

