# BFS - 미로 탐색 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/2178
from collections import deque
n,m = map(int, input().split())


arr = []
for i in range(n):
    arr.append(list(map(int,input())))

queue = deque()
queue.append((0, 0))

dr = [-1,1,0,0]
dc = [0,0,-1,1]


while queue:
    r,c = queue.popleft()

    for i in range(4):
        nr = r+dr[i]
        nc = c+dc[i]

        if 0 <= nr <n and 0 <= nc <m:
            if arr[nr][nc] ==1:
                arr[nr][nc] = arr[r][c] + 1
                queue.append((nr, nc))
print(arr[n-1][m-1])




# def move(row,col):

#     if current == move[n][m]:
#         return


#     if arr[row][col+1] == 1:
#         current = arr[row][col+1]
#         count+=1
#         move(row,col+1)


#     if arr[row+1][col] == 1:
#         current = arr[row+1][col]
#         count+=1

#         move(row+1,col)

