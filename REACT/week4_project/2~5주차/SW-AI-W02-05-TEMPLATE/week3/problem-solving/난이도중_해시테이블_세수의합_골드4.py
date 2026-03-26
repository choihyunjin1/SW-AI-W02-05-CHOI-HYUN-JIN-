# 해시 테이블 - 세 수의 합 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/2295
"""
n = int(input())
arr = []
result = 0

for i in range(n):
    arr.append(int(input()))

def serch(start, end):
    global result
    
    if end < 0:
        return
    
    for j in range(end - 1, start - 1, -1):
        for l in range(j - 1, start - 1, -1):
            for k in range(l - 1, start - 1, -1):
                result = arr[j] + arr[l] + arr[k]
                if arr[end] == result:
                    return result

serch(0, n - 1)
print(result)
"""


n = int(input())
arr = []

for i in range(n):
    arr.append(int(input()))

arr.sort()

sum_set = set()

for i in range(n):
    for j in range(n):
        sum_set.add(arr[i] + arr[j])

for d in range(n - 1, -1, -1):
    for c in range(d, -1, -1):
        if arr[d] - arr[c] in sum_set:
            print(arr[d])
            exit()
