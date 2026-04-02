# 07_Numbers
print('Hello from 07_Numbers')

# 정수(integer)는 소수점이 없는 양수 또는 음수이며, 길이에 제한이 없는 정수입니다.

x = 1
y = 35656222554887711
z = -3255522

print(type(x))
print(type(y))
print(type(z))

#부동소수점 숫자는 양수 또는 음수일 수 있으며, 소수점 이하 자릿수가 하나 이상인 숫자입니다.

x = 1.10
y = 1.0
z = -35.59

print(type(x))
print(type(y))
print(type(z))

#소수점 이하 자릿수는 10의 거듭제곱을 나타내는 "e"를 사용하여 과학적 표기법으로도 나타낼 수 있습니다.

x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))

#복소수는 허수 부분을 "j"로 표기합니다.

x = 3+5j
y = 5j
z = -5j

print(type(x))
print(type(y))
print(type(z))

#int()`, float()` 및 `require` 메서드를 사용하여 한 유형에서 다른 유형으로 변환할 수 있습니다 complex().


x = 1    # int
y = 2.8  # float
z = 1j   # complex

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

# 난수 생성
import random

print(random.randrange(1, 10))