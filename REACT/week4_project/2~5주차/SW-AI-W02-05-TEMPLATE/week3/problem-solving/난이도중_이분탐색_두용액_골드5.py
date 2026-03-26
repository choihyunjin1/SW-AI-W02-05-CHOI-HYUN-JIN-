# 이분탐색 - 두 용액 (백준 골드5)
# 문제 링크: https://www.acmicpc.net/problem/2470
n = int(input())
arr = list(map(int, input().split()))
arr.sort()

low = 0
high = n - 1

minval = abs(arr[low] + arr[high])
result1 = arr[low]
result2 = arr[high]

while low < high:
    s = arr[low] + arr[high]

    if abs(s) < minval:
        minval = abs(s)
        result1 = arr[low]
        result2 = arr[high]

    if s == 0:
        break
    elif s > 0:
        high -= 1
    else:
        low += 1

print(result1, result2)

"""
풀이용 코드 ( 정답은 나오는데 깊이제한 걸림)
n = int(input())
arr = list(map(int, input().split()))
arr.sort()



minval  = abs(arr[0]+arr[n-1])
def solve(low,high):
    
    global result1
    global result2
    global minval
    minval = abs(arr[low]+arr[high-1])
    result1 = low
    result2 = high
    if low >= high:
        return
    else:
         
        if 0 == arr[low]+arr[high]:
            result1 =low
            result2 = high
            return 
        elif 0< arr[low]+arr[high]:    
            if minval <= abs(arr[low]+arr[high]):
                solve(low,high-1)
            else: 
                minval = abs(arr[low]+arr[high])
                result1 = low 
                result2 = high
                solve(low,high-1)
        else: 
            if minval <= abs(arr[low]+arr[high]):
                solve(low+1,high)
            else: 
                minval = abs(arr[low]+arr[high])
                result1 = low 
                result2 = high
                solve(low+1,high)


solve(0,n-1)

print(f"{arr[result1]} {arr[result2]}")






"""

    

    