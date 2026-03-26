"""
Python Tuples (튜플)
튜플(Tuple)은 리스트(List)와 매우 유사하게 여러 항목을 저장하는 데 사용되는 내장 데이터 타입입니다.
하지만 가장 결정적인 차이점은 **튜플은 생성 후 변경이 불가능(Unchangeable)** 하다는 것입니다.
- 작성법: 대괄호 `[]` 대신 둥근 괄호 `()` 구문을 사용합니다.
- 순서(Ordered)가 있고, 인덱스로 접근 가능하며, 중복(Duplicates)을 허용합니다.
"""

# 예제: 튜플(Tuple) 만들기
thistuple = ("apple", "banana", "cherry")
print(thistuple)

"""
Tuple Items (튜플 항목의 특징)
- Ordered (순서가 있음): 항목들에 정의된 순서가 있으며 이 순서는 바뀌지 않습니다.
- Unchangeable (변경 불가): 튜플이 생성된 후에는 항목을 추가, 수정, 삭제할 수 없습니다. (리스트와의 결정적 차이)
- Allow Duplicates (중복 허용): 인덱스를 가지므로 똑같은 값이 여러 개 있을 수 있습니다.
"""

# 예제: 튜플은 중복 값을 허용합니다.
thistuple = ("apple", "banana", "cherry", "apple", "cherry")
print(thistuple)

"""
Tuple Length (튜플 길이)
튜플에 몇 개의 항목이 있는지 확인하려면 len() 함수를 사용합니다.
"""

# 예제: 튜플 내 항목 개수 출력하기
thistuple = ("apple", "banana", "cherry")
print(len(thistuple))

"""
 Create Tuple With One Item (항목이 단 1개뿐인 튜플 생성하기 - 매우 중요!)
항목이 오직 하나뿐인 튜플을 만들려면, 항목 뒤에 반드시 **쉼표(,)** 를 추가해야 합니다.
그렇지 않으면 파이썬은 이를 튜플로 인식하지 않고 단순한 문자열/숫자로 취급합니다.
"""

# 튜플이 맞음 (쉼표 필수): <class 'tuple'>
thistuple1 = ("apple",)
print(type(thistuple1))

# 튜플이 아님 (쉼표가 없어서 그냥 문자열로 인식됨): <class 'str'>
thistuple2 = ("apple")
print(type(thistuple2))

"""
Tuple Items - Data Types (데이터 타입)
튜플 항목은 문자열, 정수, 불리언(True/False) 등 어떤 데이터 타입이든 혼합해서 담을 수 있습니다.
"""

# 예제: 문자열, 정수, 불리언 혼합
tuple1 = ("apple", "banana", "cherry")
tuple2 = (1, 5, 7, 9, 3)
tuple3 = (True, False, False)
tuple_mixed = ("abc", 34, True, 40, "male")

"""
type() (타입 확인하기)
파이썬 관점에서 튜플은 'tuple' 이라는 데이터 타입을 가진 객체로 정의됩니다.
"""

mytuple = ("apple", "banana", "cherry")
print(type(mytuple)) # 결과: <class 'tuple'>

"""
The tuple() Constructor (tuple() 생성자 사용하기)
tuple() 이라는 내장 생성자 함수를 사용해서 자료를 튜플로 변환할 수도 있습니다.
"""

# 예제: 리스트 모양의 데이터를 tuple() 생성자로 감싸기
# 둥근 괄호가 두 번 겹쳐있음에 주의하세요: tuple((...))
thistuple = tuple(("apple", "banana", "cherry")) 
print(thistuple)

"""
---
Access Tuple Items (튜플 항목 접근하기)
리스트 항목 접근과 **완전히 동일**하게 대괄호 `[]` 안에 인덱스(순서) 번호를 참조하여 튜플 항목에 접근할 수 있습니다.
*주의: 첫 번째 항목의 인덱스는 0입니다.
"""

# 예제: 튜플의 두 번째 항목 출력 (인덱스 1)
thistuple = ("apple", "banana", "cherry")
print(thistuple[1])

"""
Negative Indexing (음수 인덱싱)
음수 인덱싱은 끝에서부터 시작함을 의미합니다.
-1은 마지막 항목, -2는 뒤에서 두 번째 항목을 나타냅니다.
"""

# 예제: 튜플의 마지막 항목 출력
thistuple = ("apple", "banana", "cherry")
print(thistuple[-1])

"""
Range of Indexes (인덱스 범위 / 슬라이싱)
어디서부터 어디까지 찾을지 지정하여 인덱스 범위를 설정할 수 있습니다. (시작:끝)
범위를 지정하면 지정된 항목들이 포함된 **새로운 튜플**이 반환됩니다.
*주의: 시작 인덱스는 포함(included)되지만 항상 끝 인덱스는 포함되지 않습니다(excluded).
"""

# 예제: 세 번째, 네 번째, 다섯 번째 항목 반환 (인덱스 2는 포함, 5는 미포함)
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:5])

# 예제: 처음부터 "kiwi" 이전까지 반환 (시작값을 생략하면 첫 항목부터 시작)
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[:4])

# 예제: "cherry"부터 끝까지 반환 (끝값을 생략하면 튜플 끝까지 포함)
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:])

"""
Range of Negative Indexes (음수 인덱스 범위)
튜플의 끝을 기준으로 검색할 때는 음수 인덱스 범위를 지정합니다.
"""

# 예제: 인덱스 -4(포함)부터 인덱스 -1(제외)까지 항목 반환
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[-4:-1])

"""
Check if Item Exists (항목 존재 여부 확인)
어떤 항목이 튜플 안에 있는지 확인하려면 `in` 키워드를 사용합니다.
"""

# 예제: 튜플에 "apple"이 있는지 확인
thistuple = ("apple", "banana", "cherry")
if "apple" in thistuple:
    print("Yes, 'apple' is in the fruits tuple")

"""
---
Python - Update Tuples (튜플 업데이트/수정하기)
튜플은 "변경 불가능(unchangeable, immutable)"합니다. 즉, 튜플이 생성된 후에는 항목을 직접 변경, 추가, 제거할 수 없습니다.
하지만 이 제한을 피해가는 유용한 방법(우회법, Workarounds)들이 있습니다.

1. Change Tuple Values (튜플 값 변경하기)
직접 수정할 수는 없지만, 튜플을 잠시 '리스트(List)'로 변환한 뒤 값을 바꾸고, 다시 '튜플'로 되돌려 놓는 방법을 사용할 수 있습니다.
"""

# 예제: 튜플을 리스트로 변환하여 항목을 변경할 수 있게 한 뒤 다시 튜플로 변환:
x = ("apple", "banana", "cherry")
y = list(x)      # 1단계: 튜플을 리스트로 바꾼다.
y[1] = "kiwi"    # 2단계: 리스트 상태에서 값을 마음대로 수정한다.
x = tuple(y)     # 3단계: 수정이 끝난 리스트를 다시 튜플로 바꾼다.
print(x)


"""
2. Add Items (항목 추가하기)
튜플은 불변이라 `append()` 같은 추가 메서드가 없습니다. 대신 두 가지 방법으로 항목을 추가할 수 있습니다.

방법 A. 리스트로 변환하기: 위의 값 변경과 동일하게, 리스트로 바꾼 뒤 `append()`로 추가하고 다시 튜플로 묶습니다.
"""

# 예제: 튜플을 리스트로 변환하고 "orange"를 추가한 후 다시 튜플로 변환:
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)
print(thistuple)

"""
방법 B. 튜플에 튜플 더하기 (+ 연산자 사용): 
튜플끼리는 서로 더해서 합칠 수 있습니다. 추가하고 싶은 값을 "1개의 항목을 가진 튜플"로 만들고 기존 튜플에 더합니다.
*(주의: 위에서 배운 대로 1개짜리 튜플을 만들 때는 꼭 끝에 쉼표(,)를 붙여야 파이썬이 튜플로 인식합니다!)*
"""

# 예제: "orange" 값을 가진 새 튜플을 생성하고, 기존 튜플에 더하기:
thistuple = ("apple", "banana", "cherry")
y = ("orange",)  # 쉼표 꼭 확인!
thistuple += y   # thistuple = thistuple + y 와 동일합니다.
print(thistuple)


"""
3. Remove Items (항목 제거하기)
튜플 내부의 특정 항목을 직접 삭제하는 것은 불가능합니다. 이것 역시 우회해야 합니다.

방법 A. 리스트로 변환하여 제거 후 다시 튜플로 변환:
"""

# 예제: 튜플을 리스트로 변환하여 `remove()`로 "apple"을 삭제한 후 다시 튜플로 변환:
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)
print(thistuple)

"""
방법 B. 튜플 자체를 완전히 삭제해버리기 (del 키워드):
내부 요소를 일부만 뺄 수는 없어도, `del` 키워드를 사용해 튜플 변수 자체를 통째로 메모리에서 삭제할 수는 있습니다.
"""

# 예제: del 키워드로 튜플 자체를 완전히 삭제하기:
thistuple = ("apple", "banana", "cherry")
del thistuple
# print(thistuple) # thistuple이 완전히 지워졌으므로 이 줄을 실행시키면 에러(NameError)가 발생합니다.

"""
---
Python - Unpack Tuples (튜플 언패킹 / 포장 풀기)

우리가 튜플을 처음 만들 때, 괄호 안에 여러 개의 값을 집어넣습니다.
마치 상자에 물건들을 담아 포장하는 것과 같아서 이를 **"Packing(패킹/포장하기)"** 이라고 부릅니다.
"""

# 예제: 튜플 패킹(Packing) - 3개의 문자열을 하나의 변수(fruits)에 담기
fruits = ("apple", "banana", "cherry")

"""
Unpacking (언패킹 / 포장 풀기)
파이썬만의 아주 강력하고 편리한 기능입니다!
튜플(상자) 안에 들어있는 여러 개의 값들을, **한 번에 여러 개의 변수로 쪼개서 각각 담아낼 수 있습니다.**
이것을 상자를 풀어 헤친다는 의미로 **"Unpacking(언패킹/포장 풀기)"** 이라고 부릅니다.
"""

# 예제: 튜플 언패킹(Unpacking)
fruits = ("apple", "banana", "cherry")

# 튜플 안에 3개의 요소가 있으므로, 왼쪽에도 3개의 변수 이름을 괄호로 묶어서 적어줍니다.
(green, yellow, red) = fruits

# 그러면 순서대로 green에는 "apple", yellow에는 "banana", red에는 "cherry"가 각각 나뉘어 들어갑니다!
print(green)   # 출력: apple
print(yellow)  # 출력: banana
print(red)     # 출력: cherry

"""
Using Asterisk * (별표 사용하기)
언패킹을 할 때, 튜플에 들어있는 항목의 개수보다 할당받을 '변수'의 개수가 모자랄 수도 있습니다.
이때 어떤 변수 이름 앞에 별표(`*`)를 붙여두면, 마치 스펀지처럼 **남은 항목들을 싹 다 흡수해서 하나의 짧은 '리스트(List)' 형태로 그 변수에 담아줍니다.**
"""

# 예제: 남은 값들을 통째로 "red" 배열(리스트)에 담기
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")

(green, yellow, *red) = fruits

print(green)   # 출력: apple
print(yellow)  # 출력: banana
print(red)     # 출력: ['cherry', 'strawberry', 'raspberry'] (리스트 형태로 묶임)

"""
별표(*)가 마지막 변수가 아니라 중간 필드에 붙어있다면 어떻게 될까요?
파이썬은 매우 똑똑하게도 마지막에 있는 변수들(예: red)의 자리를 먼저 끝에서부터 챙겨준 다음, 
가운데 애매하게 남는 나머지 값들만 별표가 붙은 변수에 리스트로 몰아넣습니다.
"""

# 예제: 중간에 남는 값들을 통째로 "tropic" 리스트에 몰아넣기
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")

(green, *tropic, red) = fruits

print(green)   # 출력: apple (첫 번째)
print(tropic)  # 출력: ['mango', 'papaya', 'pineapple'] (가운데 남는 것들 전부)
print(red)     # 출력: cherry (맨 끝자리 하나 확보)


"""
---
Loop Through a Tuple (튜플 순회하기 / 반복문 사용하기)
리스트와 완전히 동일하게, for 루프(반복문)를 사용하여 튜플의 항목들을 순회(loop)할 수 있습니다.
"""

# 예제: for 루프를 사용해 튜플 안의 항목들을 하나씩 꺼내기
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)


"""
Loop Through the Index Numbers (인덱스 번호를 통해 순회하기)
튜플 안에 있는 '값'을 직접 꺼내는 대신, '인덱스 번호(0, 1, 2...)'를 기준으로 반복문을 돌릴 수도 있습니다.
이때는 `range()`와 `len()` 함수를 조합해서 사용합니다.
"""

# 예제: range()와 len()을 이용해 인덱스 번호를 생성하고, 그 번호로 튜플 값에 접근하기
thistuple = ("apple", "banana", "cherry")

# len(thistuple)은 3이므로, range(3)은 0, 1, 2를 생성합니다.
for i in range(len(thistuple)):
  print(thistuple[i])


"""
Using a While Loop (While 루프 사용하기)
for 루프뿐만 아니라 while 루프를 사용해서도 튜플의 모든 항목을 순회할 수 있습니다.
len()으로 길이를 구하고, 0부터 시작하는 인덱스 변수 `i`를 직접 관리하며 1씩 더해줍니다.
"""

# 예제: while 루프를 사용하여 인덱스 번호로 모든 항목 살펴보기
thistuple = ("apple", "banana", "cherry")
i = 0

# i가 튜플의 전체 길이(3)보다 작을 동안 계속 반복
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1  # (핵심) 이걸 안 해주면 0번 인덱스만 평생(무한루프) 출력합니다!

"""
---
Python - Join Tuples (튜플 합치기 / 조인)
리스트에서 배웠던 것과 똑같이 `+` 연산자와 `*` 연산자를 사용하여 튜플을 합치거나 복제할 수 있습니다.

Join Two Tuples (두 개의 튜플 합치기)
두 개 이상의 튜플을 합치려면 `+` 연산자를 사용합니다.
"""

# 예제: 두 튜플 결합하기
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)

"""
Multiply Tuples (튜플 곱하기 / 복제하기)
튜플의 내용을 일정한 횟수만큼 반복해서 늘리고 싶다면(복제하고 싶다면) `*` 연산자를 사용합니다.
"""

# 예제: fruits 튜플의 내용을 2번 반복(=곱하기)해서 복제하기
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

print(mytuple)

"""
---
Tuple Methods (튜플 메서드 모음집)
튜플은 "변경 불가능(unchangeable)"하기 때문에 리스트처럼 append, remove, clear 같은 수정/삭제 메서드가 아예 존재하지 않습니다.
대신, 내용을 단순히 "조회"하거나 "검색"하는 이 2가지 내장 메서드만 가지고 있습니다. (리스트에도 동일하게 있는 메서드들입니다)

메서드     | 설명
---------|-------------------------------------------------------
count()  | 지정된 값이 튜플 안에 몇 번이나 등장하는지 그 횟수를 반환합니다.
index()  | 지정된 값을 튜플에서 찾아, 처음으로 나타나는 위치의 인덱스 번호를 반환합니다.
---
"""







