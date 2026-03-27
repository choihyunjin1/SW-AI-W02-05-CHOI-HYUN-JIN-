# 그리디 - 신입 사원 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/1946

T = int(input())

score = []

for _ in range (T):
    N = int(input())
    score = []

    for i in range(N):
        score.append(list(map(int,input().split())))

    score.sort(key = lambda x: x[0])

    count =1
    min_score = score[0][1]

    for i in range(1,N):
        if score[i][1] < min_score:
            count+=1
            min_score = score[i][1]
    print(count)

