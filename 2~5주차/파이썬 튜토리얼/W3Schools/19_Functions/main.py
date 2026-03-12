"""
Python Functions (파이썬 함수)
함수(Function)란 "호출될 때만 실행되는 코드 블록"입니다.
- 함수는 결과로 데이터를 반환(return)할 수 있습니다.
- 함수는 코드의 "반복을 피하도록" 도와주는 아주 중요한 핵심 기능입니다!
"""

print("--- Creating & Calling a Function (함수 만들고 호출하기) ---")
# 파이썬에서 함수는 `def` 키워드를 사용하여 정의(생성)합니다.
# 콜론(:) 아래에 들여쓰기된 코드가 이 함수의 내용이 됩니다.
def my_function():
  print("Hello from a function (함수에서 인사드립니다!)")

# 함수를 호출(사용)하려면 함수 이름 뒤에 괄호를 붙입니다.
my_function()
my_function() # 여러 번 반복해서 호출할 수도 있습니다!

print("\n")


"""
Function Names (함수 이름 짓는 규칙)
변수 이름을 짓는 규칙과 똑같습니다:
- 문자나 언더스코어(_)로 시작해야 합니다.
- 영문자, 숫자, 언더스코어만 포함할 수 있습니다.
- 대소문자를 구분합니다. (myFunction과 myfunction은 다른 함수입니다)
★ 함수가 무슨 동작을 하는지 알 수 있도록 '설명적인 이름'을 짓는 것이 좋은 습관입니다. (예: calculate_sum)
"""

print("--- Why Use Functions? (함수는 왜 쓸까?) ---")
print("함수를 쓰면 온도를 변환하는 것 같은 반복적인 공식을 매번 쓸 필요가 없습니다.")

# 재사용 가능한 코드 (함수 적용)
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77)) # 화씨 77도를 섭씨로
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

print("\n")


"""
Return Values (반환값 / 리턴값)
함수는 `return` 문을 사용해서, 자기를 호출했던 곳으로 "데이터를 다시 쏘아(전달해) 줄 수" 있습니다.
함수 안의 코드가 실행되다가 `return`을 만나면 그 즉시 함수는 종료되고, 뒤의 결과값을 뱉어냅니다!
"""

print("--- Return Values (값을 반환하는 함수) ---")
# 예제: 값을 반환하는 함수
def get_greeting():
  return "안녕하세요! 저는 함수가 뱉어낸 문장입니다."

# 함수가 뱉어낸(return) 값을 변수에 저장할 수 있습니다.
message = get_greeting()
print(message)

# 또는 변수 저장 없이 곧바로 print() 안에서 쓸 수도 있습니다.
print(get_greeting())

# ※ 만약 함수 안에 return 문이 없다면, 파이썬은 기본적으로 `None` 이라는 빈 값을 반환합니다.

print("\n")

"""
The pass Statement (pass 문)
if, while 문과 마찬가지로 함수(def)도 속을 비워두면 에러가 납니다.
아직 코드를 안 짰지만 나중에 짤 예정이라 자리만 만들어두려면 `pass`를 쓰면 됩니다.
"""

# 에러가 나지 않는 빈 함수 뼈대
def my_future_function():
  pass


print("\n")

"""
Arguments (인자 / 인수)
정보를 함수 내부로 전달할 수 있는데, 이를 "인자(Arguments)"라고 부릅니다.
인자는 함수 이름 뒤에 있는 괄호 안에 지정하며, 쉼표(,)로 구분하여 원하는 만큼 추가할 수 있습니다.
"""

print("--- Arguments (인자 사용하기) ---")
# fname 이라는 하나의 매개변수를 받는 함수
def print_name(fname):
  print(fname + " Refsnes")

print_name("Emil")
print_name("Tobias")
print_name("Linus")


"""
Parameters vs Arguments (매개변수 vs 인자)
두 용어는 거의 같은 뜻으로 쓰이지만, 엄밀하게 구분하자면:
- Parameter(매개변수): 함수를 '정의할 때' 괄호 안에 적어놓은 변수 (예: fname)
- Argument(인자/인수): 함수를 '호출할 때' 실제로 집어넣는 구체적인 값 (예: "Emil")
"""

print("\n--- Number of Arguments (인자의 개수) ---")
"""
함수가 2개의 인자를 받도록 정의되었다면, 호출할 때도 정확히 2개를 넘겨주어야 합니다.
덜 주거나 더 주면 에러(TypeError)가 발생합니다.
"""

def print_full_name(fname, lname):
  print(fname + " " + lname)

# 2개의 인자를 받기로 했으니 2개를 줍니다.
print_full_name("Emil", "Refsnes")
# print_full_name("Emil") # <- 이렇게 하나만 주면 에러가 납니다!


print("\n--- Default Parameter Values (매개변수 기본값 설정) ---")
"""
함수를 호출할 때 인자를 안 넘겨주면, 자동으로 사용할 "기본값"을 설정할 수 있습니다.
"""

def my_country(country = "Norway"):
  print("I am from " + country)

my_country("Sweden")
my_country("India")
my_country()      # 인자를 안 줬으므로 기본값 "Norway"가 사용됩니다!
my_country("Brazil")


print("\n--- Keyword Arguments (키워드 인자 - kwargs) ---")
"""
인자를 넘길 때 `key = value` 형태로 넘길 수 있습니다.
이 방식을 사용하면, 인자를 넘기는 "순서"는 전혀 상관없어집니다!
"""

def my_pet(animal, name):
  print(f"I have a {animal}, its name is {name}.")

# 순서를 거꾸로 넣어도 키워드를 지정했기 때문에 잘 찾아 들어갑니다.
my_pet(name = "Buddy", animal = "dog")


print("\n--- Positional Arguments (위치 인자) ---")
"""
키워드 없이 값만 순서대로 넘기는 방식을 "위치 인자"라고 합니다. 제일 첫 번째, 두 번째.. 순서가 중요합니다.
(위치 인자와 키워드 인자를 섞어 쓸 때는 "무조건 위치 인자가 먼저" 와야 합니다)
"""

def my_dog(animal, name, age):
  print(f"I have a {age} year old {animal} named {name}.")

# "dog"는 위치 인자이므로 무조건 첫 번째에 와야 하고, 나머지는 키워드로 넣음
my_dog("dog", name = "Buddy", age = 5)


print("\n--- Passing Different Data Types (다양한 자료형 넘기기) ---")
"""
숫자, 문자열뿐만 아니라 리스트, 딕셔너리 같은 모든 자료형을 함수로 휙 던질 수 있습니다!
"""

def print_foods(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
print_foods(my_fruits) # 리스트 통째로 넘기기


print("\n--- Positional-Only & Keyword-Only Arguments ---")
"""
★ 파이썬 특수 문법 (가끔 쓰입니다)
- `/,` 앞의 인자들은 "무조건 위치 인자(값만 쓰기)"로만 넘겨야 합니다.
- `*,` 뒤의 인자들은 "무조건 키워드 인자(이름=값)"로만 넘겨야 합니다.
"""

def special_func(a, b, /, *, c, d):
  return a + b + c + d

# a, b는 이름 없이 값만, c, d는 무조건 이름까지 적어줘야 합니다!
result = special_func(5, 10, c=15, d=20)
print(result)


print("\n")

"""
Arbitrary Arguments - *args (가변 위치 인자)
함수에 몇 개의 인자가 들어올지 미리 알 수 없다면, 매개변수 이름 앞에 별표(*)를 하나 붙입니다.
이렇게 하면 인자들이 함수 내부에서 하나의 "튜플(Tuple)"로 묶여서 들어옵니다!
(관례적으로 변수명을 *args 라고 많이 짓습니다)
"""

print("--- *args (개수를 모르는 인자 받기) ---")
# 예제: 원하는 만큼 아이들 이름을 받아서, 그 중 셋째를 출력하기
def my_kids_func(*kids): # *kids는 튜플 형태로 들어옵니다.
  print("가장 막내의 이름은: " + kids[2])

# 인자를 3개 던졌지만, 함수 내에서는 kids = ("Emil", "Tobias", "Linus") 가 됩니다.
my_kids_func("Emil", "Tobias", "Linus")


# 예제: 일반 매개변수와 *args 섞어 쓰기 (일반 매개변수가 먼저 와야 합니다)
def greet_people(greeting, *names):
  for name in names:
    print(greeting, name)

greet_people("Hello", "Emil", "Tobias", "Linus") # "Hello"는 greeting에, 나머지는 *names에!


print("\n--- **kwargs (가변 키워드 인자) ---")
"""
Arbitrary Keyword Arguments - **kwargs
키워드 인자(이름=값)가 몇 개 들어올지 모른다면, 매개변수 앞에 별표 두 개(**)를 붙입니다.
이렇게 하면 인자들이 함수 내부에서 하나의 "딕셔너리(Dictionary)"로 묶여서 들어옵니다!
(관례적으로 변수명을 **kwargs 라고 많이 짓습니다)
"""

# 예제: 정보를 원하는 만큼 딕셔너리로 받아오기
def print_kid_info(**kwargs):
  # kwargs는 딕셔너리가 되므로, 키를 이용해 값을 찾습니다. {"fname": "Tobias", "lname": "Refsnes"}
  print("그의 성(Last name)은 " + kwargs["lname"] + "입니다.")

print_kid_info(fname = "Tobias", lname = "Refsnes")


print("\n--- Combining *args and **kwargs (동시에 섞어서 쓰기) ---")
"""
하나의 함수에서 일반 변수, *args, **kwargs를 동시에 모두 쓸 수 있습니다.
단, 순서는 반드시 지켜야 합니다: 
1. 일반 매개변수 -> 2. *args -> 3. **kwargs
"""

def user_info(title, *args, **kwargs):
  print("Title(일반):", title)
  print("Positional(튜플로 묶임):", args)
  print("Keyword(딕셔너리로 묶임):", kwargs)

# "User Info"는 title
# "Emil", "Tobias"는 이름이 없으므로 *args
# age=25, city="Oslo"는 이름이 있으므로 **kwargs 로 들어갑니다!
user_info("User Info", "Emil", "Tobias", age=25, city="Oslo")


print("\n--- Unpacking Arguments (보따리 풀어서 넣기) ---")
"""
* 연산자와 ** 연산자를 "함수를 호출할 때" 사용하면, 
반대로 리스트나 딕셔너리의 보따리를 풀어서 하나씩 인자로 흩뿌려주는 역할(Unpacking)을 합니다.
"""

def sum_three(a, b, c):
  return a + b + c

# 1. 리스트를 풀어서 넣기 (*)
numbers = [1, 2, 3]
result = sum_three(*numbers) # == sum_three(1, 2, 3) 과 완전히 동일!
print("리스트 언패킹 결과:", result)

# 2. 딕셔너리를 풀어서 넣기 (**)
def say_hello(fname, lname):
  print("Hello", fname, lname)

person = {"fname": "Emil", "lname": "Refsnes"}
say_hello(**person) # == say_hello(fname="Emil", lname="Refsnes") 와 완전히 동일!


print("\n--- Scope (스코프: 변수의 생존 범위) ---")
"""
Python Scope
변수는 생성된 특정 '영역(Region)' 안에서만 사용할 수 있습니다. 이를 "스코프(Scope)"라고 부릅니다.
"""

print("[1. Local Scope (지역 스코프)]")
# 함수 내부에서 생성된 변수는 그 함수의 '지역 스코프'에 속하며, 오직 그 함수 내부에서만 사용할 수 있습니다.
def my_local_func():
  local_x = 300
  print(local_x) # 안에서는 잘 작동함

my_local_func()
# print(local_x) # 밖에서 부르면 에러! (지역 변수는 밖으로 못 나옴)

# Function Inside Function (함수 안의 함수)
# 지역 변수는 자기를 감싸는 함수 안의 또 다른 내부 함수에서는 사용할 수 있습니다.
def my_outer_func():
  x = 300
  def my_inner_func():
    print("내부 함수에서 접근:", x)
  my_inner_func()

my_outer_func()


print("\n[2. Global Scope (전역 스코프)]")
# 파이썬 코드의 가장 바깥쪽(메인 본문)에서 만들어진 변수를 "전역 변수"라고 합니다. 전역 변수는 어디서든 쓸 수 있습니다.
global_x = 300

def use_global():
  print("함수 내부 출력:", global_x)

use_global()
print("함수 외부 출력:", global_x)


print("\n[3. Naming Variables (같은 이름의 변수)]")
# 만약 바깥에 x가 있는데 함수 안에서 또 x를 만들면? 파이썬은 완전히 별개의 변수(동명이인)로 취급합니다.
x_var = 300 # 이건 전역 변수

def same_name_func():
  x_var = 200 # 이건 안에서만 사는 지역 변수
  print("지역 변수:", x_var)

same_name_func()
print("전역 변수는 그대로:", x_var)


print("\n[4. Global Keyword (global 키워드)]")
# 함수 내부에서 전역 변수를 아예 수정해버리고 싶다면 `global` 키워드를 씁니다.
x_target = 300 

def change_global():
  global x_target # "이건 진짜 바깥의 전역변수 x_target을 말하는 것이다!" 선언
  x_target = 200

change_global()
print("global 덕분에 바깥 값도 바뀜:", x_target)


print("\n[5. Nonlocal Keyword (nonlocal 키워드)]")
# `nonlocal`은 중첩 함수에서 사용되며, "나를 감싸고 있는 바로 바깥 함수의 변수"를 가리킵니다.
def func1():
  x = "Jane"
  def func2():
    nonlocal x
    x = "hello"
  func2()
  return x

print("nonlocal로 바뀐 값:", func1())


print("\n[6. The LEGB Rule (LEGB 규칙)]")
"""
파이썬이 일치하는 변수를 찾는 "우선순위" 입니다.
1. Local (지역): 현재 내 함수 안
2. Enclosing (둘러싼 스코프): 나를 감싸는 바깥 함수 안
3. Global (전역): 가장 바깥 메인
4. Built-in (내장): print, range 같은 기본 예약어
"""
test_var = "global"

def outer():
  test_var = "enclosing"
  def inner():
    test_var = "local"
    print("Inner:", test_var) # 1순위 local 당첨
  inner()
  print("Outer:", test_var) # 2순위 enclosing 당첨

outer()
print("Global:", test_var) # 3순위 global 당첨


print("\n--- Decorators (데코레이터: 함수 장식하기) ---")
"""
Python Decorators
데코레이터를 사용하면 원래 함수의 코드를 건드리지 않고!! "추가적인 동작"을 덧붙일 수 있습니다.
- 원리: 데코레이터 자체도 사실은 "다른 함수를 입력으로 받아서, 새로운 함수를 반환하는 함수"입니다.
- 사용법: 꾸미고 싶은 함수 바로 위에 `@데코레이터_이름` 을 적어줍니다.
"""

print("[1. Basic Decorator (기본 데코레이터)]")
# 예제: 반환되는 문자열을 무조건 대문자(UPPER)로 바꿔버리는 필터 역할을 하는 데코레이터
def changecase(func):          # func에는 밑에 있는 원래 함수가 들어옵니다.
  def myinner():               # 내부 래퍼(Wrapper) 함수
    return func().upper()      # 원래 함수를 실행한 뒤 `.upper()`를 붙여서 대문자로 만듦!
  return myinner               # 래퍼 함수를 반환

@changecase
def my_hello():
  return "Hello Sally"

print(my_hello()) # 데코레이터 덕분에 "HELLO SALLY"가 출력됩니다!


print("\n[2. Arguments in the Decorated Function (인자가 있는 함수 꾸미기)]")
# 원래 부르려던 함수에 인자가 있다면, 그걸 받아줄 래퍼(Wrapper)에도 인자가 있어야 합니다.
def changecase_with_arg(func):
  def myinner(x):                # 원래 함수가 인자(x)를 받으므로 여기서도 만들어줍니다.
    return func(x).upper()
  return myinner

@changecase_with_arg
def hello_person(name):
  return "Hello " + name

print(hello_person("John"))


print("\n[3. *args and **kwargs in Decorator (어떤 인자든 다 받아주는 데코레이터 만들기)]")
# 데코레이터를 만들 때, 원래 함수가 인자를 1개를 받을지 100개를 받을지 모른다면 *args, **kwargs를 쓰면 무적입니다!
def safe_changecase(func):
  def myinner(*args, **kwargs):
    return func(*args, **kwargs).upper() # 전부 받아서 전부 원래 함수로 토스해줍니다.
  return myinner

@safe_changecase
def hello_anyone(name):
  return "Hello " + name

print(hello_anyone("Ironman"))


print("\n[4. Decorator With Arguments (인자를 받는 데코레이터)]")
"""
데코레이터 자체에 옵션값을 주고 싶다면, 껍데기(Wrapper)를 하나 더 씌워야 합니다. (총 3중첩)
"""
def change_case_by_option(n):       # 옵션 n을 받는 최상위 함수
  def decorator(func):              # 실제 데코레이터
    def myinner():                  # 래퍼 함수
      if n == 1:
        return func().lower()       # n이 1이면 소문자로
      else:
        return func().upper()       # 아니면 대문자로
    return myinner
  return decorator

@change_case_by_option(1) # 1을 줬으므로 소문자로 바뀝니다.
def hello_linus():
  return "Hello Linus"

print(hello_linus())


print("\n[5. Multiple Decorators (데코레이터 여러 개 겹쳐 쓰기)]")
"""
하나의 함수에 여러 데코레이터를 동시에 쌓을 수 있습니다.
실행 순서는 [함수와 가장 가까운 쪽(아래쪽)]부터 먼저 적용됩니다!
"""
def addgreeting(func):
  def myinner():
    return "Hello " + func() + " Have a good day!"
  return myinner

def make_upper(func):
  def myinner():
    return func().upper()
  return myinner

@make_upper     # 2. 그런 다음 대문자로 바꿈 -> 최종: "HELLO TOBIAS HAVE A GOOD DAY!"
@addgreeting    # 1. 이게 먼저 실행됨 -> "Hello Tobias Have a good day!"
def get_name():
  return "Tobias"

print(get_name())


print("\n[6. Preserving Function Metadata (함수의 원래 정보 유지하기)]")
"""
데코레이터를 쓰고 나면 파이썬은 원래 함수가 누군지 까먹고, Wrapper 함수를 원래 함수로 착각합니다.
원래 함수의 이름이나 설명(__name__, __doc__)을 보존하려면 `functools.wraps`를 사용해야 합니다!
"""
import functools

def perfect_decorator(func):
  @functools.wraps(func)    # ★ 이 코드를 쓰면 원래 함수의 족보(메타데이터)가 보존됩니다.
  def myinner():
    return func().upper()
  return myinner

@perfect_decorator
def perfect_hello():
  return "Have a great day!"

print("함수 출력:", perfect_hello())
print("족보가 보존된 함수 이름:", perfect_hello.__name__) # 'myinner'가 아니라 'perfect_hello'가 나옵니다!


print("\n--- Python Lambda (람다: 이름 없는 한 줄 함수) ---")
"""
람다(Lambda) 함수는 작고 이름이 없는(Anonymous) 함수입니다.
원하는 만큼 매개변수(인자)를 받을 수 있지만, "표현식(수식)은 딱 하나만" 가질 수 있습니다.

문법: lambda 매개변수 : 표현식
"""

print("[1. Lambda Functions 기본 사용법]")
# 예제: 인자 a에 10을 더해서 반환하기
# 원래라면 def add_ten(a): return a + 10 해야 할 것을 다음과 같이 한 줄로 씁니다.
x = lambda a : a + 10
print("결과 (5 + 10):", x(5))

# 예제: 매개변수가 여러 개인 경우
# 인자 a와 b를 곱해서 반환 (lambda a, b : a * b)
multiply = lambda a, b : a * b
print("결과 (5 * 6):", multiply(5, 6))

# 인자 세 개(a, b, c) 더하기
sum_three_lambda = lambda a, b, c : a + b + c
print("결과 (5 + 6 + 2):", sum_three_lambda(5, 6, 2))


print("\n[2. Why Use Lambda Functions? (람다는 왜 쓸까?)]")
"""
람다의 진정한 힘은 '다른 함수 안에서 이름 없는 참모(보조 함수)로 사용될 때' 발휘됩니다.
"""
def myfunc(n):
  # 함수 안에서 '어떤 숫자(a)가 들어오면 n을 곱해주는 미완성 함수'를 반환합니다.
  return lambda a : a * n

# 1) 항상 2배로 만들어주는 함수(doubler) 탄생
mydoubler = myfunc(2) 
print("11의 2배:", mydoubler(11))

# 2) 항상 3배로 만들어주는 함수(tripler) 탄생
mytripler = myfunc(3)
print("11의 3배:", mytripler(11))
# => 잠깐 쓰고 버릴 간단한 함수가 필요할 때 람다를 씁니다.


print("\n[3. Lambda with Built-in Functions (내장 함수와 함께 쓰는 람다)]")
"""
람다는 파이썬의 대표적인 내장 함수인 map(), filter(), sorted() 와 찰떡궁합입니다!
"""

# ① map() 함수: 리스트의 모든 요소에 동일한 함수(규칙)를 적용합니다.
numbers1 = [1, 2, 3, 4, 5]
# 모든 요소에 2를 곱해라 (lambda x: x * 2)
doubled = list(map(lambda x: x * 2, numbers1))
print("map()으로 2배 만들기:", doubled)


# ② filter() 함수: 리스트에서 "조건이 참(True)"인 것들만 걸러냅니다.
numbers2 = [1, 2, 3, 4, 5, 6, 7, 8]
# 어떤 수 x를 2로 나눈 나머지가 0이 아니면(홀수이면) 통과!
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers2))
print("filter()로 홀수만 남기기:", odd_numbers)


# ③ sorted() 함수: 람다를 사용해 "자신만의 커스텀 정렬 기준"을 만들 수 있습니다.
# 예제: 튜플의 '두 번째 요소(나이)'를 기준으로 정렬하기
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
# 기준(key): 전달된 튜플(x)의 인덱스 1번 자리 (나이)
sorted_students = sorted(students, key=lambda x: x[1])
print("나이순으로 정렬된 학생들:", sorted_students)

# 예제: 문자열의 '길이'를 기준으로 정렬하기
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print("글자 길이순으로 정렬된 단어들:", sorted_words)


print("\n--- Python Recursion (재귀 함수: 자기 자신을 호출하는 함수) ---")
"""
Recursion (재귀)
수학과 프로그래밍에서 흔히 쓰이는 개념으로, 함수가 자기 자신을 다시 호출하는 것을 의미합니다.
*주의: 잘못 작성하면 영원히 끝나지 않거나(무한 루프), 메모리를 엄청나게 잡아먹지만,
완벽하게 작성하면 굉장히 효율적이고 수학적으로 아름다운 코드가 됩니다.
"""

print("[1. Basic Recursion (기본 재귀)]")
# 예제: 5부터 0까지 카운트다운 하는 함수
def countdown(n):
  if n <= 0: # 멈추는 조건
    print("Done!")
  else:
    print(n)
    countdown(n - 1) # 자기 자신한테 '나보다 1 작은 숫자'를 줘서 다시 실행시킴!

countdown(5)


print("\n[2. Base Case and Recursive Case (종료 조건과 재귀 조건)]")
"""
모든 재귀 함수는 무조건 2가지 구조를 가져야만 합니다! (안 그러면 컴퓨터 터집니다)
1. Base case(기본/종료 조건): 재귀를 멈추고 거꾸로 값을 반환하기 시작하는 브레이크
2. Recursive case(재귀 조건): 인자를 변형시켜서 자기 자신을 부르는 엑셀
"""

# 예제: 팩토리얼 구하기 (5! = 5 * 4 * 3 * 2 * 1)
def factorial(n):
  # 1. Base case: 0이나 1이 되면 멈추고 1을 내뱉음
  if n == 0 or n == 1:
    return 1
  # 2. Recursive case: 아직 안 끝났으면 n * (나보다 1 작은 팩토리얼)
  else:
    return n * factorial(n - 1)

print("5 팩토리얼:", factorial(5))


print("\n[3. Fibonacci Sequence (피보나치 수열)]")
# 앞의 두 숫자를 더해서 현재 숫자를 만드는 유명한 수열 (0, 1, 1, 2, 3, 5, 8, 13...)
def fibonacci(n):
  # Base case: 0이나 1이면 자기 자신을 그대로 내뱉음
  if n <= 1:
    return n
  # Recursive case: 앞의 수(n-1)와 앞앞의 수(n-2)를 더함!
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)

print("피보나치 수열의 7번째 숫자:", fibonacci(7)) # 13


print("\n[4. Recursion with Lists (리스트와 재귀)]")
# 반복문 없이 리스트를 처리할 수 있습니다. 한 번에 하나씩 떼어내서 처리!

# 예제 1: 리스트의 모든 요소 더하기
def sum_list(numbers):
  if len(numbers) == 0:     # 더 이상 남은 게 없으면 0을 돌려줌
    return 0
  else:
    # 첫 번째 요소 + 나머지 요소들([1:])의 합
    return numbers[0] + sum_list(numbers[1:])

print("리스트 요소의 합:", sum_list([1, 2, 3, 4, 5]))


# 예제 2: 리스트에서 가장 큰 값 찾기
def find_max(numbers):
  if len(numbers) == 1:     # 한 개만 남았으면 그게 제일 큰 거니까 반환
    return numbers[0]
  else:
    max_of_rest = find_max(numbers[1:]) # 첫 번째 빼고 나머지 중에 제일 큰 거 찾아와!
    # 첫 번째 놈이랑 나머지 중 제일 큰 놈이랑 비교해서 더 큰 놈을 반환
    return numbers[0] if numbers[0] > max_of_rest else max_of_rest

print("리스트 통틀어 가장 큰 값:", find_max([3, 7, 2, 9, 1]))


print("\n[5. Recursion Depth Limit (파이썬의 재귀 깊이 제한)]")
"""
파이썬은 컴퓨터가 다운되는 걸 막기 위해, 함수가 자기 자신을 호출할 수 있는 최대 횟수를 막아두었습니다.
기본 Limit은 보통 1,000번입니다 (1000번 이상 자기 자신 안으로 들어가면 에러 `RecursionError` 발생).
"""
import sys

# 현재 설정된 재귀 한도 확인하기
print("현재 파이썬 재귀 한계:", sys.getrecursionlimit())

# 한도를 임의로 늘릴 수 있지만, 너무 늘리면 파이썬이 Crash(튕김) 현상이 날 수 있습니다.
sys.setrecursionlimit(2000)
print("재귀 한계 2000으로 늘린 후:", sys.getrecursionlimit())


print("\n--- Python Generators (제너레이터: 일시정지 가능한 함수) ---")
"""
Generators (제너레이터)
일반 함수가 `return`을 만나면 완전히 종료되어버리는 것과 달리, 
제너레이터는 실행을 "일시정지(pause)"하고 나중에 그 지점부터 다시 "재개(resume)"할 수 있는 함수입니다.
특징: 이 함수를 호출하면, 코드가 바로 실행되는 게 아니라 반복 가능한 '제너레이터 객체'가 반환됩니다.
"""

print("[1. The yield Keyword (yield 키워드)]")
"""
함수 안에 `return` 대신 `yield`가 있으면 그 함수는 제너레이터가 됩니다.
yield를 만나면 현재의 '상태(로컬 변수 등)'를 저장해둔 채 멈추고 값을 뱉어냅니다!
"""

def my_generator():
  yield 1
  yield 2
  yield 3

# for 문을 통해 반복할 때마다 차례대로 1, 2, 3이 나옴
print("기본 제너레이터 출력:")
for value in my_generator():
  print(value)


print("\n[2. Generators Saves Memory (메모리 절약의 마법사)]")
"""
리스트는 [1, 2, 3 ... 100만] 의 백만 개 숫자를 메모리에 전부 통째로 올려놔야 하지만,
제너레이터는 "다음에 무슨 숫자가 나올지 공식만 알고 있고, 달라고 할 때마다 하나씩 계산해서 줌" 방식이므로
메모리(RAM)를 거의 쓰지 않습니다!
"""
def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1

print("5까지 세기:")
for num in count_up_to(5):
  print(num)


print("\n[3. Using next() with Generators (next() 함수 사용하기)]")
"""
for 문 없이 한 건씩 수동으로 뽑아오고 싶을 때 `next()`를 사용합니다.
더 이상 내뱉을 `yield`가 없는데도 `next()`를 부르면 `StopIteration` 에러가 납니다.
"""
def simple_gen():
  yield "Emil"
  yield "Tobias"
  yield "Linus"

gen = simple_gen() # 1. 함수를 불러서 제너레이터 '객체'를 장전함
print(next(gen))   # 2. 첫 번째 yield 실행하고 일시정지 -> "Emil"
print(next(gen))   # 3. 마저 실행하다 두 번째 yield 만나서 멈춤 -> "Tobias"
print(next(gen))   # 4. 세 번째 -> "Linus"
# print(next(gen)) # 5. 더 이상 없으니까 여기서 StopIteration 에러 발생!


print("\n[4. Generator Expressions (제너레이터 식)]")
"""
리스트 컴프리헨션(List Comprehension) 문법에서 대괄호 `[]` 대신
소괄호 `()`를 쓰면 그 즉시 '제너레이터'가 만들어집니다.
"""
list_comp = [x * x for x in range(5)] # 메모리에 리스트 [0, 1, 4, 9, 16] 이 툭 떨어짐
print("리스트:", list_comp)

gen_exp = (x * x for x in range(5)) # 메모리에 리스트가 없음! (요청 시 계산할 준비만 되어있음)
print("제너레이터 객체:", gen_exp)
print("제너레이터 리스트화:", list(gen_exp)) # 달라고 하니까 그제야 0, 1, 4, 9, 16을 줌

# sum 같은 내장 함수와 쓸 때 메모리도 아끼고 아주 훌륭합니다.
total = sum(x * x for x in range(10))
print("제곱의 합계:", total)


print("\n[5. Fibonacci Sequence Generator (무한 피보나치 제너레이터)]")
"""
제너레이터를 쓰면 "무한 반복(while True)" 패턴을 안전하게 만들 수 있습니다. (메모리 터질 일이 없음)
"""
def fibonacci_gen():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b

fib_gen = fibonacci_gen()
print("피보나치 첫 10개만 뽑아보기:")
for _ in range(10):
  print(next(fib_gen), end=" ")
print()


print("\n[6. Generator Methods - send() & close() (심화 조작)]")
"""
- send(값): 일시정지 된 제너레이터 내부로 "값을 집어넣으면서" 깨웁니다!
- close(): 제너레이터 작업을 강제로 완전히 종료시킵니다.
"""
def echo_generator():
  while True:
    received = yield # 밖에서 send()로 보낸 값을 received가 받음
    print("내부에 전달받은 값:", received)

echo_gen = echo_generator()
next(echo_gen) # Prime: 한 번 돌려서 `yield` 위치까지 대기시켜놔야 입력을 받을 수 있음.

echo_gen.send("Hello")
echo_gen.send("World")

echo_gen.close() # 안전하게 종료




