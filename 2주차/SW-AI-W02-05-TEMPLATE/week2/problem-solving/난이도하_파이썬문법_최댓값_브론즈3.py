# 파이썬 문법 - 최댓값 (백준 브론즈3)
# 문제 링크: https://www.acmicpc.net/problem/2562
a = []
max =0
count = 0
for i in range (9):
    b = int(input())
    a.append(b)

max = a[0]
for j in range (9):
    if max < a[j]:
        max = a[j]
        count =j


print(max)
print(count+1)


