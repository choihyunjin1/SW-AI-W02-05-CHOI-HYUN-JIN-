# 스택 - 탑 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/2493
import sys

n = int(sys.stdin.readline())
heights = list(map(int, sys.stdin.readline().split()))

from typing import List, Tuple

stack: List[Tuple[int, int]] = [] 
answer: List[int] = []

for i in range(n):
    current_height = heights[i]

    while stack and stack[-1][1] < current_height:
        stack.pop()

    if stack:
        answer.append(stack[-1][0])
    else:
        answer.append(0)

    stack.append((i + 1, current_height))

print(*answer)