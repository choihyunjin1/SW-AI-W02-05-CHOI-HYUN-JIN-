# 10_Booleans
print('Hello from 10_Booleans')

# 불리언(Boolean) 값
# 프로그래밍에서는 표현식이 True인지 False인지 알아야 할 때가 많습니다.
# 파이썬에서는 어떤 표현식이든 평가하여 True 또는 False 중 하나의 대답을 얻을 수 있습니다.

# 두 값을 비교할 때 표현식이 평가되고 파이썬은 불리언 답을 반환합니다:
print(10 > 9)
print(10 == 9)
print(10 < 9)

# if 문에서 조건을 실행하면 파이썬은 True 또는 False를 반환합니다:
# 조건이 True인지 False인지에 따라 메시지를 출력합니다:
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# 값과 변수 평가
# bool() 함수를 사용하면 모든 값을 평가하고 True 또는 False를 반환받을 수 있습니다.

# 문자열과 숫자 평가:
print(bool("Hello"))
print(bool(15))

# 두 변수 평가:
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

# 대부분의 값은 True입니다
# 거의 모든 값은 어떤 내용이든 있으면 True로 평가됩니다.
# 빈 문자열을 제외한 모든 문자열은 True입니다.
# 0을 제외한 모든 숫자는 True입니다.
# 비어 있는 것을 제외한 모든 리스트, 튜플, 세트, 딕셔너리는 True입니다.

# 다음은 True를 반환합니다:
print(bool("abc")) # 원문 예제 (프린트로 감쌈)
print(bool(123))
print(bool(["apple", "cherry", "banana"]))

# 일부 값은 False입니다
# 사실, (), [], {}, "", 숫자 0, None과 같은 빈 값들을 제외하고는 False로 평가되는 값은 많지 않습니다. 
# 그리고 당연히 False 값 자체도 False로 평가됩니다.

# 다음은 False를 반환합니다:
print(bool(False)) # 원문 예제 (프린트로 감쌈)
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

# 또 다른 예로, __len__ 함수가 0 또는 False를 반환하는 클래스로 만든 객체가 있다면 False로 평가됩니다:
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

# 함수는 불리언을 반환할 수 있습니다
# 불리언 값을 반환하는 함수를 만들 수 있습니다:
def myFunction() :
  return True

print(myFunction())

# 함수의 불리언 답을 기반으로 코드를 실행할 수 있습니다:
# 예제: 함수가 True를 반환하면 "YES!"를 출력하고, 그렇지 않으면 "NO!"를 출력합니다:
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

# 파이썬에는 객체가 특정 데이터 유형인지 여부를 확인하는 데 사용할 수 있는 isinstance() 함수와 같이 
# 불리언 값을 반환하는 많은 내장 함수도 있습니다:
# 예제: 객체가 정수인지 아닌지 확인합니다:
x = 200
print(isinstance(x, int))
