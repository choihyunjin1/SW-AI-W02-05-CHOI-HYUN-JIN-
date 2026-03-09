# 정수론 - 소수 찾기 (백준 브론즈2)
# 문제 링크: https://www.acmicpc.net/problem/1978
n = int(input())
a = []
count = 0

a = list(map(int, input().split()))

for j in range(n):
    tmp = 0
    for d in range(1, a[j]):
        if a[j] % d == 0:
            tmp += 1

    if tmp == 1:
        count += 1

print(count)


        