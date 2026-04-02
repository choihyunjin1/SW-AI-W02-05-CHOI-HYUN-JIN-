# 트리 - 트리 만들기 (백준 실버4)
# 문제 링크: https://www.acmicpc.net/problem/14244

class TreeNode:
    """이진 트리 노드"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

n,m = map(int,input().split())
k = 2 + n-m


for i in range(k-1):
    print(i, i+1)

for i in range(k, n):
    print(1, i)