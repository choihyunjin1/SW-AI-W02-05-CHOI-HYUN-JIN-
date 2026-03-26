sum =0
for i in range (11):
    sum += i

print(sum)



def exp(b, n):
    if n == 0:
        return 1
    else:
        b*exp(b, n-1)
    

    
def expp(b, n):
    if n == 0:
        return 1
    elif n%2 == 1:
        return b * expp(b,n-1)
    else:
        return expp(b, n//2)*expp(b, n//2)
    
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def chp(amount,coins):
    if amount ==0:
        return 1
    if amount <0 or len(coins) == 0:
        return 0
    return
        chp(amount==, coins[1:])+ chp)