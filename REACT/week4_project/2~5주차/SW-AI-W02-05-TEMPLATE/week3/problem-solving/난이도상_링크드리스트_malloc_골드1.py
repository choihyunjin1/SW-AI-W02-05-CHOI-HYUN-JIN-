# 링크드리스트 - malloc (백준 골드1)
# 문제 링크: https://www.acmicpc.net/problem/3217
import sys

input = sys.stdin.readline

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        self

text = input().rstrip()
m = int(input())

head = Node('')
tail = Node('')

head.next = tail
tail.prev = head

cursor = head
for ch in text:
    new_node = Node(ch)

    new_node.prev = cursor
    new_node.next = tail

    cursor.next = new_node
    tail.prev = new_node

    cursor = new_node


for _ in range(m):
    command = input().rstrip()

    if command[0] == 'L':
       

    elif command[0] == 'D':
        

    elif command[0] == 'B':
       

          

    elif command[0] == 'P':
      

result = []
current = head.next

while current != tail:
    

print(''.join(result))
