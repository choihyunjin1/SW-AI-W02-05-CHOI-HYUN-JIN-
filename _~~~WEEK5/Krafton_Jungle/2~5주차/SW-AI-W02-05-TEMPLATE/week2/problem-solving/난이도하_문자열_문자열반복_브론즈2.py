# 문자열 - 문자열 반복 (백준 브론즈2)
# 문제 링크: https://www.acmicpc.net/problem/2675

num = int(input())
result = []

for i in range(num):
    R, S = input().split()
    R = int(R)

    temp = ""
    for c in S:
        temp += c * R
    
    result.append(temp)

for r in result:
    print(r)