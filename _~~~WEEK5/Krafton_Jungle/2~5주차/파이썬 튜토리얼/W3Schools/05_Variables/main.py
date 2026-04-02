# 05_Variables
print('Hello from 05_Variables')
x= 5
y ="choi"

print(x)
print(y)

x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)



x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0


x = 5
y = "John"
print(type(x))
print(type(y))



x = "John"
# is the same as
x = 'John'


a = 4
A = "Sally"
#변수는 대소문자 구분함



# 카멜 케이스
# 첫 번째 단어를 제외한 모든 단어는 대문자로 시작합니다.

# myVariableName = "John"
# 파스칼 사건
# 각 단어는 모두 대문자로 시작합니다.

# MyVariableName = "John"
# 뱀 케이스
# 각 단어는 밑줄 문자로 구분됩니다.

# my_variable_name = "John"


x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
# 한번에 여러 변수 사용 가능


fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)
# 변수에 할당된 값의 수와 변수의 수가 일치해야 합니다.
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)


x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

x = "awesome"



# 지역 변수와 전역 변수
def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)



# 전역 변수는 함수 밖에서 정의되고 모든 함수에서 사용할 수 있습니다.
# 지역 변수는 함수 내에서 정의되고 해당 함수 내에서만 사용할 수 있습니다.
# 함수 내에서 전역 변수를 사용하려면 global 키워드를 사용해야 합니다.
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)