# 11_Operators
print('Hello from 11_Operators')

x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)

# --- 파이썬 산술 연산자 ---
# +	덧셈 (Addition)		x + y	
# -	뺄셈 (Subtraction)	x - y	
# *	곱셈 (Multiplication)	x * y	
# /	나눗셈 (Division)		x / y	
# %	나머지 (Modulus)		x % y	
# **	거듭제곱 (Exponentiation)	x ** y	
# //	버림 나눗셈 (몫, Floor division)	x // y





numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")


# --- 파이썬 할당 연산자 (Assignment Operators) ---
# =		x = 5			x = 5	
# +=		x += 3			x = x + 3	
# -=		x -= 3			x = x - 3	
# *=		x *= 3			x = x * 3	
# /=		x /= 3			x = x / 3	
# %=		x %= 3			x = x % 3	
# //=		x //= 3			x = x // 3	
# **=		x **= 3			x = x ** 3	
# &=		x &= 3			x = x & 3	
# |=		x |= 3			x = x | 3	
# ^=		x ^= 3			x = x ^ 3	
# >>=		x >>= 3			x = x >> 3	
# <<=		x <<= 3			x = x << 3	
# :=		print(x := 3)		x = 3; print(x) (바다코끼리 연산자, Walrus Operator)
x = 5
y = 3

# --- 파이썬 비교 연산자 (Comparison Operators) ---
# ==	같음 (Equal)				x == y	
# !=	같지 않음 (Not equal)			x != y	
# >	큼 (Greater than)			x > y	
# <	작음 (Less than)			x < y	
# >=	크거나 같음 (Greater than or equal)	x >= y	
# <=	작거나 같음 (Less than or equal)	x <= y

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

print(1 < x < 10)

print(1 < x and x < 10)


# --- 파이썬 논리 연산자 (Logical Operators) ---
# and   두 조건이 모두 참이면 True 반환                   x < 5 and x < 10
# or    두 조건 중 하나라도 참이면 True 반환              x < 5 or x < 4
# not   결과를 반대로 뒤집음 (참이면 False, 거짓이면 True)  not(x < 5 and x < 10)

x = 5

# 예제: 숫자가 0보다 크고 10보다 작은지 테스트 (and 연산자)
print(x > 0 and x < 10)

# 예제: 숫자가 5보다 작거나 10보다 큰지 테스트 (or 연산자)
print(x < 5 or x > 10)

# 예제: not을 사용하여 결과 반전시키기
print(not(x > 3 and x < 10))


# --- 파이썬 식별 연산자 (Identity Operators) ---
# is       두 변수가 같은 객체인 경우 True 반환                 x is y
# is not   두 변수가 같은 객체가 아닌 경우 True 반환              x is not y

# 예제: is 연산자는 두 변수가 같은 객체를 가리키면 True를 반환합니다.
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z) # True (동일한 객체를 가리킴)
print(x is y) # False (값은 같지만, 메모리 상의 다른 객체임)
print(x == y) # True (값 자체가 같음)

# 예제: is not 연산자는 두 변수가 같은 객체를 가리키지 않으면 True를 반환합니다.
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y) # True (다른 객체이므로)

# is 와 == 의 차이점
# is - 메모리 상에서 두 변수가 동일한 객체를 가리키는지 확인합니다.
# == - 두 변수의 "값(value)"이 동일한지 확인합니다.

# 예제
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y) # True (값이 같음)
print(x is y) # False (값은 같으나 다른 객체임)


# --- 파이썬 멤버십 연산자 (Membership Operators) ---
# 멤버십 연산자는 어떤 시퀀스(연속된 값)가 객체 안에 존재하는지 테스트하는 데 사용됩니다.
# in        지정된 값을 가진 시퀀스가 객체 안에 존재하면 True 반환         x in y
# not in    지정된 값을 가진 시퀀스가 객체 안에 존재하지 않으면 True 반환    x not in y

# 예제: "banana"가 리스트 안에 존재하는지 확인
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits) # True 반환

# 예제: "pineapple"이 리스트 안에 존재하지 **않는지** 확인
fruits = ["apple", "banana", "cherry"]
print("pineapple" not in fruits) # True 반환 (없으므로)

# 문자열에서의 멤버십
# 멤버십 연산자는 문자열에서도 똑같이 작동합니다.
text = "Hello World"

print("H" in text)     # True 반환 (대문자 'H'가 존재함)
print("hello" in text) # False 반환 (소문자 'hello'는 존재하지 않음, 대소문자 구분)
print("z" not in text) # True 반환 ('z'가 존재하지 않으므로)


# --- 파이썬 비트 연산자 (Bitwise Operators) ---
# 비트 연산자는 2진수(이진수) 숫자를 비교하는 데 사용됩니다.
# & 	AND (논리곱)			두 비트가 모두 1이면 각 비트를 1로 설정합니다.		x & y	
# |	OR (논리합)			두 비트 중 하나라도 1이면 각 비트를 1로 설정합니다.	x | y	
# ^	XOR (배타적 논리합)		두 비트 중 하나만 1인 경우 각 비트를 1로 설정합니다.	x ^ y	
# ~	NOT (논리부정)			모든 비트를 반전시킵니다.				~x	
# <<	Zero fill left shift (왼쪽 시프트)	오른쪽에서 0을 밀어 넣어 왼쪽으로 이동시키고 가장 왼쪽 비트는 떨어져 나갑니다.	x << 2	
# >>	Signed right shift (오른쪽 시프트)	왼쪽에서 가장 왼쪽 비트의 복사본을 밀어 넣어 오른쪽으로 이동시키고 가장 오른쪽 비트는 떨어져 나갑니다.	x >> 2	

# 예제 (& 연산자)
# & 연산자는 각 비트를 비교하여 둘 다 1이면 1로 설정하고, 그렇지 않으면 0으로 설정합니다:
print(6 & 3)
# 6의 이진수 표현: 0110
# 3의 이진수 표현: 0011
# & 연산자는 비트를 비교하고 0010을 반환하며, 이는 십진수로 2입니다.

# 예제 (| 연산자)
# | 연산자는 각 비트를 비교하여 하나 또는 두 개가 모두 1이면 1로 설정하고, 그렇지 않으면 0으로 설정합니다:
print(6 | 3)
# 6의 이진수 표현: 0110
# 3의 이진수 표현: 0011
# | 연산자는 비트를 비교하고 0111을 반환하며, 이는 십진수로 7입니다.

# 예제 (^ 연산자)
# ^ 연산자는 각 비트를 비교하여 하나만 1일 때 1로 설정하고, 그렇지 않으면(둘 다 1이거나 둘 다 0일 때) 0으로 설정합니다:
print(6 ^ 3)
# 6의 이진수 표현: 0110
# 3의 이진수 표현: 0011
# ^ 연산자는 비트를 비교하고 0101을 반환하며, 이는 십진수로 5입니다.


# --- 연산자 우선순위 (Operator Precedence) ---
# 연산자 우선순위는 연산이 수행되는 순서를 설명합니다.

# 예제: 괄호는 가장 높은 우선순위를 가지므로, 괄호 안의 표현식이 가장 먼저 평가되어야 합니다.
print((6 + 3) - (6 + 3))

# 예제: 곱셈(*)은 덧셈(+)보다 높은 우선순위를 가지므로, 덧셈보다 곱셈이 먼저 평가됩니다.
print(100 + 5 * 3)

# 우선순위 순서 (Precedence Order)
# 아래 표는 가장 높은 우선순위부터 순서대로 나열한 것입니다:
# 1. ()		괄호 (Parentheses)
# 2. **		거듭제곱 (Exponentiation)
# 3. +x -x ~x	단항 양수, 단항 음수, 비트 NOT (Unary plus, unary minus, and bitwise NOT)
# 4. * / // %	곱셈, 나눗셈, 버림 나눗셈(몫), 나머지 (Multiplication, division, floor division, and modulus)
# 5. + -		덧셈과 뺄셈 (Addition and subtraction)
# 6. << >>		비트 왼쪽/오른쪽 시프트 (Bitwise left and right shifts)
# 7. &		비트 AND (Bitwise AND)
# 8. ^		비트 XOR (Bitwise XOR)
# 9. |		비트 OR (Bitwise OR)
# 10. == != > >= < <= is is not in not in (비교, 식별, 멤버십 연산자)
# 11. not		논리 NOT (Logical NOT)
# 12. and		논리 AND (AND)
# 13. or		논리 OR (OR)

# 좌에서 우로 평가 (Left-to-Right Evaluation)
# 두 연산자가 동일한 우선순위를 가지면, 표현식은 왼쪽에서 오른쪽으로 평가됩니다.

# 예제: 덧셈(+)과 뺄셈(-)은 같은 우선순위를 가지므로 왼쪽에서 오른쪽으로 표현식을 평가합니다.
print(5 + 4 - 7 + 3)

