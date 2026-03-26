# 분할정복 - 색종이 만들기 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/2630

n = int(input())
paper = []
for _ in range(n):
    paper.append(list(map(int, input().split())))

w = 0
b = 0

def solve(x, y, size):
    global w, b

    color = paper[x][y]
    
    for i in range(x, x + size):
        for j in range(y, y + size):
            if paper[i][j] != color:
                half = size // 2
                solve(x, y, half)
                solve(x, y + half, half)
                solve(x + half, y, half)
                solve(x + half, y + half, half)
                return

    if color == 0:
        w += 1
    else:
        b += 1


solve(0, 0, n)

print(w)
print(b)