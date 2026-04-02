# 그리디 - 잃어버린 괄호 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/1541
s = input()

part = s.split("-")

result = sum(map(int,part[0].split("+")))

for p in part[1:]:
    result -= sum(map(int, p.split('+')))

print(result)