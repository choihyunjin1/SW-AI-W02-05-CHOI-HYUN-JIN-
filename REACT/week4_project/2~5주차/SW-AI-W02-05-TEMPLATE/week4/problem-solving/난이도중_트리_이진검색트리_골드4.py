# 트리 - 이진 검색 트리 (백준 골드4)
# 문제 링크: https://www.acmicpc.net/problem/5639


import sys
sys.setrecursionlimit(10**6)

tree = []

while True:
    line = sys.stdin.readline()
    
    if not line:  # 입력 끝
        break

    if line.strip() == "":
        break

    tree.append(int(line))


def postorder(tree):
    if not tree:
        return
    
    root = tree[0]
    idx = len(tree)
    for i in range(1, len(tree)):
            if root < tree[i]:
                idx = i
                break
    left = tree[1:idx]
    right = tree[idx:]

    postorder(left)
    postorder(right)
    print(root)


postorder(tree)