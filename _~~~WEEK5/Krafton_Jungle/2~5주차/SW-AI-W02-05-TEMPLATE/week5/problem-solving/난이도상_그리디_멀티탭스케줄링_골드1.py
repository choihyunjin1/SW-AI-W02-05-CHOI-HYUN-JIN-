# 그리디 - 멀티탭 스케줄링 (백준 골드1)
# 문제 링크: https://www.acmicpc.net/problem/1700
n, k = map(int, input().split())

multi = list(map(int, input().split()))
cnt = 0

result = []

for i in range(k):
    if multi[i] in result:
        continue

    if len(result) < n:
        result.append(multi[i])
        continue

    idx = -1
    farthest = -1

    for j in range(n):
        if result[j] not in multi[i+1:]:
            idx = j
            break
        else:
            next_use = multi[i+1:].index(result[j])
            if next_use > farthest:
                farthest = next_use
                idx = j

    result[idx] = multi[i]
    cnt += 1

print(cnt)