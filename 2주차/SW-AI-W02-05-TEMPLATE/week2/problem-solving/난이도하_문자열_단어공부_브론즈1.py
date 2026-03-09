# 문자열 - 단어 공부 (백준 브론즈1)
# 문제 링크: https://www.acmicpc.net/problem/1157

RAW = input()
result =""
duply = RAW.upper()

count = {}
for ch in duply:
    if ch in count:
        count[ch] += 1
    else:
        count[ch] = 1

maxcnt = 0


max_value = max(count.values())
for key, value in count.items():
    if value == max_value:
        maxcnt += 1
        result = key

if maxcnt > 1:
    print("?")
else:    
    print(result)