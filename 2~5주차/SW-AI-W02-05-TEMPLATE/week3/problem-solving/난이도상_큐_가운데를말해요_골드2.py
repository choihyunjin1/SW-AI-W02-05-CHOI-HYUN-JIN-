# 큐 - 가운데를 말해요 (백준 골드2)
# 문제 링크: https://www.acmicpc.net/problem/1655

# n = int(input())
# list =[]

# for i in range(1,n+1):
#     list.append(int(input()))
#     list.sort()
#     mid = (i) //2
#     if len(list) % 2 == 0:
#         print(f"{list[mid]}")
#     else :
#         print(f"{list[mid]}")


# 힙 - 가운데를 말해요 (백준 골드2)
# 문제 링크: https://www.acmicpc.net/problem/1655

import sys
import heapq

n = int(sys.stdin.readline())

left = []   
right = []  

for _ in range(n):
    num = int(sys.stdin.readline())

    if len(left) == len(right):
        heapq.heappush(left, -num)
    else:
        heapq.heappush(right, num)

    if right and (-left[0] > right[0]):
        left_top = -heapq.heappop(left)
        right_top = heapq.heappop(right)

        heapq.heappush(left, -right_top)
        heapq.heappush(right, left_top)

 
    print(-left[0])