# 정수론 - 골드바흐의 추측 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/9020
prime = [True] * 10001
prime[0] = prime[1] = False

for i in range(2, 101):
    if prime[i]:
        for j in range(i*i, 10001, i):
            prime[j] = False

t = int(input())

for _ in range(t):
    n = int(input())
    left = n // 2
    right = n // 2

    while True:
        if prime[left] and prime[right]:
            
            break
        left -= 1
        right += 1
    print(left, right)    
