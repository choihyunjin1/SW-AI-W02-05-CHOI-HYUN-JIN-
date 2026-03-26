# 링크드리스트 - 철도 공사 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/23309
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
stations = list(map(int, input().split()))

MAX = 1000000 + 1
prev_station = [0] * MAX
next_station = [0] * MAX

for i in range(n):
    now = stations[i]
    prev_station[now] = stations[i - 1]
    next_station[now] = stations[(i + 1) % n]

answer = []

for _ in range(m):
    cmd = input().split()

    if cmd[0] == 'BN':
        i = int(cmd[1])
        j = int(cmd[2])

        nxt = next_station[i]
        answer.append(str(nxt))

        next_station[i] = j
        prev_station[j] = i
        next_station[j] = nxt
        prev_station[nxt] = j

    elif cmd[0] == 'BP':
        i = int(cmd[1])
        j = int(cmd[2])

        prv = prev_station[i]
        answer.append(str(prv))

        next_station[prv] = j
        prev_station[j] = prv
        next_station[j] = i
        prev_station[i] = j

    elif cmd[0] == 'CN':
        i = int(cmd[1])

        target = next_station[i]
        answer.append(str(target))

        new_next = next_station[target]
        next_station[i] = new_next
        prev_station[new_next] = i

    elif cmd[0] == 'CP':
        i = int(cmd[1])

        target = prev_station[i]
        answer.append(str(target))

        new_prev = prev_station[target]
        prev_station[i] = new_prev
        next_station[new_prev] = i

print('\n'.join(answer))
