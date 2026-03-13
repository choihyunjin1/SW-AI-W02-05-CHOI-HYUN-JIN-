# 스택 - 스택 (백준 실버 4)
# 문제 링크: https://www.acmicpc.net/problem/10828
import sys

n = int(sys.stdin.readline())
stack = []
result = []

for _ in range(n):
    command = sys.stdin.readline().rstrip()

    if command[:4] == "push":
        num = int(command[5:])
        stack.append(num)

    elif command == "pop":
        if stack == []:
            result.append("-1")
        else:
            result.append(str(stack.pop()))

    elif command == "size":
        result.append(str(len(stack)))

    elif command == "empty":
        if stack == []:
            result.append("1")
        else:
            result.append("0")

    elif command == "top":
        if stack == []:
            result.append("-1")
        else:
            result.append(str(stack[-1]))

print("\n".join(result))