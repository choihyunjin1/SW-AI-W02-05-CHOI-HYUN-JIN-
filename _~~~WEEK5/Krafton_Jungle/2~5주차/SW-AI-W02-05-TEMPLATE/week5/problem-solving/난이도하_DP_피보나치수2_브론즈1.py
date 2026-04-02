# DP - 피보나치 수 2 (백준 브론즈 1)
# 문제 링크: https://www.acmicpc.net/problem/2748

def fib_memo(n,memo = None):
        if memo == None:
            memo = {}


        if n in memo:
            return memo[n]
       
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        if n>1:
            memo[n] = fib_memo(n-1,memo)+fib_memo(n-2,memo)
            return memo[n]
    
n = int(input())

print(fib_memo(n))