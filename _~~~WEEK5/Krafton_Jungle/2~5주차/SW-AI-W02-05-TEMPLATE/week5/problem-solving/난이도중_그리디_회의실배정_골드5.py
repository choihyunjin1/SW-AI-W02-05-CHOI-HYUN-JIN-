# 그리디 - 회의실 배정 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/1931
def select_meetings(meetings):

    
    if meetings == []:
        return 0
    
    meetings.sort(key=lambda x: (x[1], x[0]))
    selected = []
    
    selected.append(meetings[0])
    last_end = meetings[0][1]
    
    for i in range(1, len(meetings)):
        if meetings[i][0] >= last_end:
            selected.append(meetings[i])
            last_end = meetings[i][1]

    
    return len(selected)

n = int(input())
time = []
for _ in range(n):
    time.append(list(map(int,input().split())))

print(select_meetings(time))