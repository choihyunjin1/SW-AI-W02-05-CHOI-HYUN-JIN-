# 큐 - 카드2 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/2164
from collections import deque

n = int(input())
list = []
for i in range(1,n+1):
    list.append(i)
card = deque(list)

for _ in range (n-1):
    card.popleft()
    card.append(card.popleft())

print(card.pop())


