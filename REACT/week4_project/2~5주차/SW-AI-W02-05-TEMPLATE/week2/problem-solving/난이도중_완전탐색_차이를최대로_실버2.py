# 완전탐색 - 차이를 최대로 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/10819

n = int(input())                      # [1] 입력 받기
a = list(map(int, input().split()))  # [1] 입력 받기

max_value = 0                        # [2] 최댓값 저장 변수 준비
used = [False] * n                   # [3] 사용 여부 체크 배열 준비


def dfs(path):                       # [4] 현재까지 만든 순열 상태를 들고 DFS 시작
    global max_value                 # [2] 바깥의 max_value를 같이 사용

    if len(path) == n:               # [5] 순열이 완성되었는지 확인
        total = 0                    # [6] 식 계산 시작
        for i in range(len(path) - 1):   # [6] 인접한 원소끼리 비교
            total += abs(path[i] - path[i + 1])   # [6] |A[i]-A[i+1]| 누적

        if total > max_value:        # [7] 최댓값 갱신 확인
            max_value = total        # [7] 더 크면 갱신
        return                       # [8] 계산 끝났으니 이전 단계로 돌아감

    for i in range(n):               # [9] 다음에 넣을 숫자 후보 전부 확인
        if not used[i]:              # [10] 아직 안 쓴 숫자인가?
            used[i] = True           # [11] 사용 표시
            path.append(a[i])        # [11] 현재 순열에 추가

            dfs(path)                # [12] 다음 자리 만들러 내려감

            path.pop()               # [13] 되돌리기
            used[i] = False          # [13] 사용 표시 해제


dfs([])                              # [14] 빈 순열에서 시작
print(max_value)                     # [15] 정답 출력


"""
초기 상태: calc = [], visited = [0, 0, 0]

(idx = 0)
├── [i=0 선택] calc = [0], visited = [1, 0, 0]
│   │
│   (idx = 1)
│   ├── [i=1 선택] calc = [0, 1], visited = [1, 1, 0]
│   │   │
│   │   (idx = 2)
│   │   └── [i=2 선택] calc = [0, 1, 2], visited = [1, 1, 1]
│   │        n=3 도달! (Basis part 실행)
│   │        계산: |array[0]-array[1]| + |array[1]-array[2]| 
│   │        계산: |10-20| + |20-30| = 20 (max_value 갱신)
│   │        return 후 백트래킹 (calc.pop() 실행 -> calc=[0, 1], visited=[1, 1, 0])
│   │
│   ├── [i=2 선택] calc = [0, 2], visited = [1, 0, 1]
│   │   │
│   │   (idx = 2)
│   │   └── [i=1 선택] calc = [0, 2, 1], visited = [1, 1, 1]
│   │        n=3 도달! (Basis part 실행)
│   │        계산: |array[0]-array[2]| + |array[2]-array[1]|
│   │        계산: |10-30| + |30-20| = 30 (max_value = 30으로 갱신)
│   │        return 후 백트래킹 
│
(idx = 0)
├── [i=1 선택] calc = [1], visited = [0, 1, 0]
│   ├── ... (위와 동일한 방식으로 [1, 0, 2], [1, 2, 0] 탐색)
│
(idx = 0)
└── [i=2 선택] calc = [2], visited = [0, 0, 1]
    ├── ... (동일하게 [2, 0, 1], [2, 1, 0] 탐색)
    """