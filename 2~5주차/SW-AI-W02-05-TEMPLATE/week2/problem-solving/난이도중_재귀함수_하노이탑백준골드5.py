# 재귀함수 - 하노이 탑 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/1914
def dohanoi(n, start, end, tmp):
    if n == 1:
        print(start, end)
        return
    
    dohanoi(n - 1, start, tmp, end)
    print(start, end)
    dohanoi(n - 1, tmp, end, start)

n = int(input())

print(2 ** n - 1)
if n <= 20:
    dohanoi(n, 1, 3, 2)