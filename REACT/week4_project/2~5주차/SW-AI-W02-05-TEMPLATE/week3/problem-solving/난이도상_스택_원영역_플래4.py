# 스택 - 원 영역 (백준 플래4)
# 문제 링크: https://www.acmicpc.net/problem/10000
import sys
input = sys.stdin.readline

N = int(input())
circles = []

for _ in range(N):
    x, r = map(int, input().split())
    left = x - r
    right = x + r
    circles.append((left, right))

circles.sort(key=lambda x: (x[0], -x[1]))

stack = []
ans = 1


for l, r in circles:
    while stack and stack[-1][1] <= l:
        cl, cr, filed =stack.pop()
        ans +=1
        if filed == cr:
            ans += 1

        if stack and stack[-1][2] == cl:
            stack[-1][2] = cr
    stack.append([l, r, l])

while stack:
    cl, cr, filed = stack.pop()
    ans += 1
    if filed == cr:
        ans += 1
    if stack and stack[-1][2] == cl:
        stack[-1][2] = cr
print(ans)