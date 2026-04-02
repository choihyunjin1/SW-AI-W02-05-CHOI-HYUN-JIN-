# 큐 - 뱀 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/3190
from collections import deque

n = int(input())
k = int(input())

board = [[0] * n for _ in range(n)]

for _ in range(k):
    x, y = map(int, input().split())
    board[x - 1][y - 1] = 1  

l = int(input())
turns = {}

for _ in range(l):
    x, c = input().split()
    turns[int(x)] = c


dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

direction = 0   
time = 0

snake = deque()
snake.append((0, 0))
board[0][0] = 2  

while True:
    time += 1

    head_x, head_y = snake[-1]
    nx = head_x + dx[direction]
    ny = head_y + dy[direction]

    if nx < 0 or nx >= n or ny < 0 or ny >= n:
        break

    if board[nx][ny] == 2:
        break

    if board[nx][ny] == 1:
        board[nx][ny] = 2
        snake.append((nx, ny))

    else:
        board[nx][ny] = 2
        snake.append((nx, ny))

        tail_x, tail_y = snake.popleft()
        board[tail_x][tail_y] = 0

    if time in turns:
        if turns[time] == 'D':
            direction = (direction + 1) % 4
        else:  # 'L'
            direction = (direction - 1) % 4

print(time)