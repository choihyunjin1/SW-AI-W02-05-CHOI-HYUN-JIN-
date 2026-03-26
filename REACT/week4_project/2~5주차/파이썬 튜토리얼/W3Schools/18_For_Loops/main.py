"""
Python For Loops (파이썬 For 반복문)
for 반복문은 시퀀스(리스트, 튜플, 딕셔너리, 세트, 또는 문자열)를 처음부터 끝까지 순회(반복)하는 데 사용됩니다.
while 문과 달리 인덱싱 변수(i=0 등)를 미리 설정해둘 필요가 없어서, 컬렉션을 다룰 때 훨씬 직관적입니다.
"""

print("--- 리스트 요소 반복하기 ---")
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

print("\n")


"""
Looping Through a String (문자열 반복하기)
문자열(String)도 하나하나의 문자가 모인 시퀀스이기 때문에 순회할 수 있는(iterable) 객체입니다.
"""

print("--- 문자열 요소 반복하기 ---")
# 예제: "banana"라는 단어의 각 알파벳을 한 줄씩 출력합니다.
for x in "banana":
  print(x)

print("\n")


"""
The break Statement (break 문)
break 문을 사용하면, 리스트 등의 모든 요소를 채 다 돌기 전에 반복문을 아예 끝내고 강제 탈출할 수 있습니다!
"""

print("--- break 문 (출력 후 확인하여 탈출) ---")
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    print("-> banana를 출력하고 루프 탈출!")
    break

print("\n--- break 문 (출력 전에 확인하여 탈출) ---")
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    print("-> banana를 만났으므로 출력 안 하고 바로 루프 탈출!")
    break
  print(x)

print("\n")


"""
The continue Statement (continue 문)
continue 문을 사용하면, 현재 반복 스텝은 멈추지만, 전체 루프를 끝내지는 않고 "다음 요소"로 바로 건너뜁니다!
"""

print("--- continue 문 ---")
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    print("-> banana는 건너뜁니다!")
    continue # 아래 print(x)를 무시하고 반복문의 처음(다음 과일)으로 올라갑니다.
  print(x)

print("\n")


"""
The range() Function (range() 함수 ★아주 많이 씁니다★)
특정한 횟수만큼 코드를 반복시키고 싶을 때는 range() 함수를 사용합니다.
- 기본값: 0에서 시작하고, 1씩 증가합니다.
- 주의: range(6) 은 1~6이 아니라, 0~5까지만 반환합니다! (6의 직전에 끝남)
"""

print("--- range(6) 사용 (0부터 5까지 총 6번) ---")
for x in range(6):
  print(x)

print("\n--- 시작값 지정: range(2, 6) ---")
# 2부터 5까지 출력 (6 미만)
for x in range(2, 6):
  print(x)

print("\n--- 증가폭 지정: range(2, 30, 3) ---")
# 2부터 29까지 3씩 증가 (2, 5, 8, ... 29)
for x in range(2, 30, 3):
  print(x)

