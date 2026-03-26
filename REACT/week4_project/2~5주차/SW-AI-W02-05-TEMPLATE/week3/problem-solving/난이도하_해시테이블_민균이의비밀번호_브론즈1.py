# 해시 테이블 - 민균이의 비밀번호 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/9933
n= int(input())

word=[]
for _ in range (n):
    word.append(input())






for i in word:
    revers = i[::-1]
    if revers in word:
        print(len(i), i[len(i)//2])
        break
