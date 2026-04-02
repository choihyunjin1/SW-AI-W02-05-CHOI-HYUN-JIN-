"""
Python range (파이썬 range)
내장 함수인 range()는 불변(immutable) 숫자 시퀀스를 반환하며, 일반적으로 특정 횟수만큼 반복할 때 사용됩니다.

이 숫자 집합은 `range`라는 자체 데이터 타입을 가집니다.

참고: 불변(Immutable)이란 생성된 후에 수정할 수 없음을 의미합니다.

Ranges 생성하기 (Creating ranges)
range() 함수는 1개, 2개 또는 3개의 인수를 사용하여 호출할 수 있으며, 구문은 다음과 같습니다:

range(start, stop, step)

1. 하나의 인수로 range() 호출하기
range 함수가 하나의 인수로만 호출되면, 해당 인수는 종료(stop) 값을 나타냅니다.
시작(start) 인수는 선택 사항이며, 제공되지 않으면 기본값인 0으로 설정됩니다.
range(10)은 0부터 9까지의 각 숫자 시퀀스를 반환합니다. (시작 인수인 0은 포함되고, 종료 인수인 10은 포함되지 않습니다).
"""

print("--- 하나의 인수로 range() 호출 ---")
# 예제: 0부터 9까지의 숫자 범위 생성하기
x = range(10)
print(list(x))


"""
2. 두 개의 인수로 range() 호출하기
range 함수가 두 개의 인수로 호출되면, 첫 번째 인수는 시작(start) 값을, 두 번째 인수는 종료(stop) 값을 나타냅니다.
range(3, 10)은 3부터 9까지의 각 숫자 시퀀스를 반환합니다.
"""

print("\n--- 두 개의 인수로 range() 호출 ---")
# 예제: 3부터 9까지의 숫자 범위 생성하기
x = range(3, 10)
print(list(x))


"""
3. 세 개의 인수로 range() 호출하기
range 함수가 세 개의 인수로 호출되면, 세 번째 인수는 단계(step) 값을 나타냅니다.
단계(step) 값은 시퀀스의 각 숫자 간의 차이를 의미합니다. 선택 사항이며, 제공되지 않으면 기본값인 1로 설정됩니다.
range(3, 10, 2)는 3부터 9까지의 각 숫자 시퀀스를 2의 단계로 반환합니다.
"""

print("\n--- 세 개의 인수로 range() 호출 ---")
# 예제: 3부터 9까지 2씩 증가하는 숫자 범위 생성하기
x = range(3, 10, 2)
print(list(x))


"""
Ranges 사용하기 (Using ranges)
Range는 종종 for 루프에서 숫자 시퀀스를 반복하는 데 사용됩니다.
"""

print("\n--- Ranges 사용하기 ---")
# 예제: range의 각 값을 반복하기
for i in range(10):
  print(i, end=' ')
print() # 줄바꿈


"""
리스트를 사용하여 Ranges 표시하기 (Using List to Display Ranges)
range 객체는 불변 숫자 시퀀스를 나타내는 데이터 타입이므로, 직접 화면에 표시할 수 없습니다.
따라서, range는 화면에 표시하기 위해 리스트로 변환되는 경우가 많습니다.
"""

print("\n--- 리스트를 사용하여 Ranges 표시 ---")
# 예제: 다양한 range를 리스트로 변환하기
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(5, 20, 3)))


"""
Ranges 슬라이싱 (Slicing Ranges)
다른 시퀀스들과 마찬가지로, range도 하위 시퀀스를 추출하기 위해 슬라이싱할 수 있습니다.
"""

print("\n--- Ranges 슬라이싱 ---")
# 예제: range에서 하위 시퀀스 추출하기
r = range(10)
print("r[2]:", r[2])
print("r[:3]:", r[:3])
# 참고: 첫 번째 print 문은 인덱스 2의 값을 반환하고, 두 번째 print 문은 인덱스 0부터 3 미만까지의 새로운 range 객체를 반환합니다.


"""
멤버십 테스트 (Membership Testing)
Range는 `in` 연산자를 사용하여 멤버십 테스트를 지원합니다.
"""

print("\n--- 멤버십 테스트 ---")
# 예제: 숫자 6과 7이 range에 존재하는지 테스트하기
r = range(0, 10, 2)
print("6 in r:", 6 in r)
print("7 in r:", 7 in r)
# 반환 값은 숫자가 range에 존재하면 True, 그렇지 않으면 False를 의미합니다.


"""
길이 (Length)
Range는 range 내의 요소 개수를 얻기 위해 len() 함수를 지원합니다.
"""

print("\n--- 길이 ---")
# 예제: range의 길이 구하기
r = range(0, 10, 2)
print("len(r):", len(r))

