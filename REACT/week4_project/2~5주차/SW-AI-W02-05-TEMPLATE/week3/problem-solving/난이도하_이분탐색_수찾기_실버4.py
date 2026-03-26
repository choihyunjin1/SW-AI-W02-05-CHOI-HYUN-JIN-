# 이분탐색 - 수 찾기 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/1920
n = int(input())
num_list = list(map(int, input().split()))
num_list.sort()

def serch(left, right):
    if left > right:
        return 0

    mid = (left + right) // 2

    if j == num_list[mid]:
        return 1
    elif j > num_list[mid]:
        return serch(mid + 1, right)
    else:
        return serch(left, mid - 1)

m = int(input())
targets = list(map(int, input().split()))

for j in targets:
    print(serch(0, n - 1))