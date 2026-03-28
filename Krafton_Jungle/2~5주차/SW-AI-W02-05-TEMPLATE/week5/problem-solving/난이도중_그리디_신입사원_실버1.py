# 그리디 - 신입 사원 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/1946

import sys
input = sys.stdin.readline

T = int(input())
result = []

for _ in range(T):
    N = int(input())

    score_list = []
    for i in range(N):
        score_list.append(tuple(map(int, input().split())))

    paper_sorted = sorted(score_list, key=lambda x: x[0])

    interview_sorted = sorted(score_list, key=lambda x: x[1])

    interview_rank = {}
    for i in range(N):
        interview_rank[interview_sorted[i]] = i                        
                                                                                            #     interview_rank = {
                                                                                            #     (4,1): 0,
                                                                                            #     (3,2): 1,
                                                                                            #     (2,3): 2,
                                                                                            #     (1,4): 3 }
                                                                                            # 
                                                                                            #  score_list
                                                                                            #    
                                                                                            # paper_sorted  (서류 기준 정렬)
                                                                                            # interview_sorted ->  interview_rank (면접 순위표)
                                                                                            #    
                                                                                            # for score in paper_sorted:
                                                                                            #     interview_rank[score] vs min_rank 비교
 
    count = 0
    min_rank = N 
    # [ (1,4), (2,3), (3,2), (4,1) ]
    #      4      3     2      1
    # [ (2,3), (3,2), (4,1) ]
    for score in paper_sorted:
        if interview_rank[score] < min_rank:
            count += 1
            min_rank = interview_rank[score]

    result.append(count)

for i in result:
    print(i)


# import sys
# input = sys.stdin.readline

# T = int(input())

# for _ in range(T):
#     N = int(input())
#     score = []

#     for i in range(N):
#         score.append(list(map(int, input().split())))

#     score.sort(key=lambda x: x[1])
#     score.sort(key=lambda x: x[0])

#     count = 1
#     min_score = score[0][1]

#     for i in range(1, N):
#         if score[i][1] < min_score:
#             count += 1
#             min_score = score[i][1]

#     print(count)

