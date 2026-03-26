"""
Python Math (파이썬 수학)
파이썬에는 폭넓은 수학 모듈을 포함하여 숫자에 대한 수학적 작업을 수행할 수 있는 내장 수학 함수 세트가 있습니다.

내장 수학 함수 (Built-in Math Functions)
min() 및 max() 함수는 이터러블(iterable)에서 가장 낮거나 가장 높은 값을 찾는 데 사용할 수 있습니다.
"""

print("--- min() 및 max() 함수 ---")
# 예제: 최솟값과 최댓값 찾기
x = min(5, 10, 25)
y = max(5, 10, 25)

print("min(5, 10, 25):", x)
print("max(5, 10, 25):", y)


"""
abs() 함수는 지정된 숫자의 절대값(양수)을 반환합니다.
"""

print("\n--- abs() 함수 (절대값) ---")
# 예제: -7.25의 절대값 구하기
x = abs(-7.25)
print("abs(-7.25):", x)


"""
pow(x, y) 함수는 x의 y제곱(x^y) 값을 반환합니다.
"""

print("\n--- pow() 함수 (제곱) ---")
# 예제: 4의 3제곱 (4 * 4 * 4 와 동일) 값을 반환하기
x = pow(4, 3)
print("pow(4, 3):", x)


"""
The Math Module (수학 모듈)
파이썬에는 수학 함수 목록을 확장하는 math라는 내장 모듈도 있습니다.
이것을 사용하려면 math 모듈을 가져와야(import) 합니다: import math

math 모듈을 가져오면 해당 모듈의 메서드와 상수를 사용할 수 있습니다.
예를 들어, math.sqrt() 메서드는 숫자의 제곱근을 반환합니다.
"""

print("\n--- math 모듈: sqrt() 제곱근 ---")
# 예제: math 모듈을 임포트하고 64의 제곱근 구하기
import math

x = math.sqrt(64)
print("math.sqrt(64):", x)


"""
math.ceil() 메서드는 숫자를 가장 가까운 정수로 올림하고, 
math.floor() 메서드는 숫자를 가장 가까운 정수로 내림하여 결과를 반환합니다.
"""

print("\n--- math 모듈: ceil() 올림과 floor() 내림 ---")
# 예제: 1.4를 각각 올림, 내림하기
import math

x = math.ceil(1.4)
y = math.floor(1.4)

print("math.ceil(1.4):", x) # 2 반환
print("math.floor(1.4):", y) # 1 반환


"""
math.pi 상수는 PI 값(3.141592...)을 반환합니다.
"""

print("\n--- math 모듈: pi 상수 ---")
# 예제: PI 값 구하기
import math

x = math.pi
print("math.pi:", x)

