# 링크드리스트 - 에디터 (백준 실버2)
# 문제 링크: https://www.acmicpc.net/problem/1406
import sys

input = sys.stdin.readline

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


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
        if cursor != head:
            cursor = cursor.prev

    elif command[0] == 'D':
        if cursor.next != tail:
            cursor = cursor.next

    elif command[0] == 'B':
        if cursor != head:
            delete_node = cursor
            left_node = delete_node.prev
            right_node = delete_node.next

            left_node.next = right_node
            right_node.prev = left_node

            cursor = left_node

    elif command[0] == 'P':
        ch = command[2]

        new_node = Node(ch)
        right_node = cursor.next

        new_node.prev = cursor
        new_node.next = right_node

        cursor.next = new_node
        right_node.prev = new_node

        cursor = new_node

result = []
current = head.next

while current != tail:
    result.append(current.data)
    current = current.next

print(''.join(result))
