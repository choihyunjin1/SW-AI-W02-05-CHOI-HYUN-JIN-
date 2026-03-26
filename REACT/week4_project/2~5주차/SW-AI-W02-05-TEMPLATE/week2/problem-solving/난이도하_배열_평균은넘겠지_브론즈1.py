# 배열 - 평균은 넘겠지 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/4344

num = int(input())
result = []

for i in range(num):
    a = list(map(int, input().split()))

    cnt = a[0]
    scores = a[1:]

    sum = 0
    for j in range(cnt):
        sum += scores[j]

    avg = sum / cnt

    avgcnt = 0
    for d in range(cnt):
        if scores[d] > avg:
            avgcnt += 1

    ovweavg = avgcnt / cnt * 100

    result.append("%.3f%%" % ovweavg)

for x in result:
    print(x)