# 문자열 - IPv6 (백준 실버1)
# 문제 링크: https://www.acmicpc.net/problem/3107
ip = input()
if "::" in ip:


    left, right = ip.split("::")
    if left != "":
        leftlist = left.split(":")
    else: leftlist = []


    rightlist = right.split(":")


    missing = 8- (len(rightlist) + len(leftlist))
    middle = []
    for i in range(missing):
        middle.append("0000")


    for le in range(len(leftlist)):
        leftlist[le] = leftlist[le].zfill(4)

    for ri in range(len(rightlist)):
        rightlist[ri] =  rightlist[ri].zfill(4)

    group = leftlist + middle + rightlist

else:
    group = ip.split(":")
    for i in range(len(group)):
        group[i] = group[i].zfill(4)



result = ":".join(group)

print(result)