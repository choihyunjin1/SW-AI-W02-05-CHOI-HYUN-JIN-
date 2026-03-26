"""
Python Loops (파이썬의 반복문)
파이썬에는 두 가지 기본 반복문 명령어가 있습니다:
1. while 반복문
2. for 반복문

The while Loop (while 반복문)
while 반복문을 사용하면 조건이 참(True)인 동안 일련의 명령문들을 계속해서 실행할 수 있습니다.
※ 주의: 증감식(예: i += 1)을 잊지 마세요! 그렇지 않으면 반복문이 영원히 실행됩니다(무한 루프).
"""

print("--- 기본 while 문 ---")
# 예제: i가 6보다 작은 동안 i를 출력합니다.
i = 1

# while 루프는 관련 변수가 미리 준비되어 있어야 합니다. (여기서는 인덱싱 변수 i를 1로 설정함)
while i < 6:
  print(i)
  i += 1  # 이 부분이 없으면 i는 평생 1이므로 영원히 출력됩니다!

print("\n")


"""
The break Statement (break 문)
break 문을 사용하면, while 조건이 여전히 참(True)이더라도 
강제로 반복문을 멈추고 빠져나올 수 있습니다.
"""

print("--- break 문 ---")
# 예제: i가 3이 될 때 루프를 종료(탈출)합니다.
i = 1
while i < 6:
  print(i)
  if i == 3:
    print("i가 3이 되어서 break로 탈출합니다!")
    break
  i += 1

print("\n")


"""
The continue Statement (continue 문)
continue 문을 사용하면 현재 반복(스텝)을 중단하고,
건너뛴 다음 반복문의 처음으로 돌아가 다음 스텝을 계속 진행합니다.
"""

print("--- continue 문 ---")
# 예제: i가 3일 때는 밑의 코드를 무시하고 다음 반복으로 건너뜁니다.
i = 0
while i < 6:
  i += 1
  if i == 3:
    print("i가 3이라서 출력 안 하고 continue로 건너뜁니다!")
    continue
  print(i)

print("\n")


"""
The else Statement (else 문 - while과 함께 사용)
while 문 뒤에 else 문을 사용하면, 
조건이 더 이상 참이 아닐 때(반복이 정상적으로 종료되었을 때) 
특정 코드 블록을 한 번 실행할 수 있습니다. 

(단, break로 강제 종료되었을 때는 else 블록이 실행되지 않습니다.)
"""

print("--- while - else 문 ---")
# 예제: 조건이 거짓이 되면 메시지를 출력합니다.
i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("조건(i < 6)이 거짓이 되어 루프가 정상적으로 끝났습니다! (i는 더 이상 6보다 작지 않음)")

