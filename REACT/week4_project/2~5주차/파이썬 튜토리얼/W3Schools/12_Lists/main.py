# 12_Lists
print('Hello from 12_Lists')

# List (리스트)
# 리스트는 단일 변수에 여러 항목을 저장하는 데 사용됩니다.
# 리스트는 파이썬에서 데이터의 모음을 저장하는 데 사용되는 4가지 기본 데이터 유형 중 하나입니다.
# 나머지 3개는 튜플(Tuple), 세트(Set), 딕셔너리(Dictionary)이며 모두 각기 다른 품질과 용도를 가지고 있습니다.

# 리스트는 대괄호 []를 사용하여 만듭니다:

# 예제: 리스트 생성
thislist = ["apple", "banana", "cherry"]
print(thislist)

# 리스트 항목 (List Items)
# 리스트 항목은 순서가 있고, 변경할 수 있으며, 중복된 값을 허용합니다.
# 리스트 항목은 인덱싱됩니다. 첫 번째 항목의 인덱스는 [0], 두 번째 항목의 인덱스는 [1] 등입니다.

# Ordered (순서가 있음)
# 리스트에 순서가 있다는 것은 항목이 정의된 순서를 가지고 있으며, 그 순서가 바뀌지 않는다는 것을 의미합니다.
# 리스트에 새 항목을 추가하면 새 항목은 리스트의 맨 끝에 배치됩니다.
# (참고: 순서를 바꾸는 일부 리스트 메서드가 있지만, 일반적으로 항목의 순서는 변하지 않습니다.)

# Changeable (변경 가능함)
# 리스트는 변경 가능합니다. 즉, 리스트가 만들어진 후에 리스트의 항목을 변경, 추가, 제거할 수 있습니다.

# Allow Duplicates (중복 허용)
# 리스트는 인덱싱되어 있기 때문에 동일한 값을 가진 항목을 가질 수 있습니다:

# 예제: 리스트는 중복된 값을 허용합니다
thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)

# List Length (리스트 길이)
# 리스트에 몇 개의 항목이 있는지 확인하려면 len() 함수를 사용합니다:

# 예제: 리스트에 있는 항목의 수를 출력
thislist = ["apple", "banana", "cherry"]
print(len(thislist))

# List Items - Data Types (리스트 항목 - 데이터 유형)
# 리스트 항목은 모든 데이터 유형이 될 수 있습니다:

# 예제: 문자열, 정수, 불리언 데이터 유형
list1 = ["apple", "banana", "cherry"]
list2 = [1, 5, 7, 9, 3]
list3 = [True, False, False]

# 리스트는 다른 데이터 유형을 함께 포함할 수도 있습니다:
# 예제: 문자열, 정수, 불리언 값을 모두 가진 리스트
list1 = ["abc", 34, True, 40, "male"]

# type() (데이터 유형 확인)
# 파이썬의 관점에서 보았을 때 리스트는 'list'라는 데이터 유형을 가진 객체(object)로 정의됩니다:
# <class 'list'>

# 예제: 리스트의 데이터 유형은 무엇입니까?
mylist = ["apple", "banana", "cherry"]
print(type(mylist))

# The list() Constructor (list() 생성자)
# 새 리스트를 만들 때 list() 생성자를 사용할 수도 있습니다.

# 예제: list() 생성자를 사용하여 리스트 만들기
thislist = list(("apple", "banana", "cherry")) # 이중 둥근 괄호(()) 사용에 주의하세요
print(thislist)

# Access Items (항목 접근)
# 리스트 항목은 인덱싱되어 있으며, 인덱스 번호를 참조하여 항목에 접근할 수 있습니다:

# 예제: 리스트의 두 번째 항목 출력
thislist = ["apple", "banana", "cherry"]
print(thislist[1])
# 참고: 첫 번째 항목의 인덱스는 0입니다.

# Negative Indexing (음수 인덱싱)
# 음수 인덱싱은 끝에서부터 시작한다는 의미입니다.
# -1은 마지막 항목을 나타내고, -2는 뒤에서 두 번째 항목을 나타냅니다.

# 예제: 리스트의 마지막 항목 출력
thislist = ["apple", "banana", "cherry"]
print(thislist[-1])

# Range of Indexes (인덱스 범위)
# 범위를 시작할 위치와 끝낼 위치를 지정하여 인덱스 범위를 지정할 수 있습니다.
# 범위를 지정할 때 반환 값은 지정된 항목이 포함된 새 리스트입니다.

# 예제: 세 번째, 네 번째, 다섯 번째 항목 반환
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])
# 참고: 검색은 인덱스 2(포함)에서 시작하여 인덱스 5(포함되지 않음)에서 끝납니다.
# 첫 번째 항목의 인덱스는 0임을 기억하세요.

# 시작 값을 생략하면 범위는 첫 번째 항목부터 시작됩니다:
# 예제: 이 예제는 처음부터 "kiwi"를 포함하지 **않는** 위치까지 항목을 반환합니다:
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[:4])

# 끝 값을 생략하면 범위는 리스트의 끝까지 진행됩니다:
# 예제: 이 예제는 "cherry"부터 끝까지 항목을 반환합니다:
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:])

# Range of Negative Indexes (음수 인덱스 범위)
# 리스트 끝에서부터 검색을 시작하려면 음수 인덱스를 지정하세요:

# 예제: 이 예제는 "orange" (-4)부터 "mango" (-1)을 포함하지 **않는** 위치까지 차례대로 항목을 반환합니다.
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[-4:-1])

# Check if Item Exists (항목 존재 여부 확인)
# 리스트에 특정 항목이 있는지 확인하려면 'in' 키워드를 사용하세요:

# 예제: "apple"이 리스트에 있는지 확인
thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

# Change List Items (리스트 항목 변경)
# 항목 값 변경
# 특정 항목의 값을 변경하려면 인덱스 번호를 참조하세요:

# 예제: 두 번째 항목 변경
thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)

# 항목 값 범위 변경
# 특정 범위 내의 항목 값을 변경하려면, 새 값이 포함된 리스트를 정의하고 새 값을 삽입할 인덱스 번호 범위를 참조하세요:

# 예제: "banana"와 "cherry" 값을 "blackcurrant"와 "watermelon" 값으로 변경
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

# 교체하려는 항목보다 더 많은 항목을 삽입하면, 지정한 위치에 새 항목이 삽입되고 남은 항목은 그에 맞게 이동합니다:
# 예제: 두 번째 값을 두 개의 새 값으로 변경
thislist = ["apple", "banana", "cherry"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)
# 참고: 삽입된 항목 수와 교체된 항목 수가 다르면 리스트의 길이는 변경됩니다.

# 교체하려는 항목보다 더 적은 항목을 삽입하면, 지정한 위치에 새 항목이 삽입되고 남은 항목은 그에 맞게 이동합니다:
# 예제: 두 번째와 세 번째 값을 하나의 값으로 변경
thislist = ["apple", "banana", "cherry"]
thislist[1:3] = ["watermelon"]
print(thislist)

# Insert Items (항목 삽입)
# 기존 값을 교체하지 않고 새 리스트 항목을 삽입하려면 insert() 메서드를 사용할 수 있습니다.
# insert() 메서드는 지정된 인덱스에 항목을 삽입합니다:

# 예제: "watermelon"을 세 번째 항목으로 삽입
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)

# Append Items (항목 추가)
# 리스트의 끝에 항목을 추가하려면 append() 메서드를 사용합니다:

# 예제: append() 메서드를 사용하여 항목 추가하기
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

# Insert Items (항목 삽입)
# 지정된 인덱스에 리스트 항목을 삽입하려면 insert() 메서드를 사용합니다.

# 예제: 항목을 두 번째 위치에 삽입하기
thislist = ["apple", "banana", "cherry"]
thislist.insert(1, "orange")
print(thislist)
# 참고: 위 예제들의 결과로 리스트는 이제 4개의 항목을 포함하게 됩니다.

# Extend List (리스트 확장)
# 다른 리스트의 요소를 현재 리스트에 추가하려면 extend() 메서드를 사용합니다.

# 예제: tropical의 요소들을 thislist에 추가하기
thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)
# 요소들은 리스트의 끝에 추가됩니다.

# Add Any Iterable (모든 반복 가능한 객체 추가)
# extend() 메서드는 꼭 리스트만 추가해야 하는 것은 아니며, 모든 반복 가능한(iterable) 객체(튜플, 세트, 딕셔너리 등)를 추가할 수 있습니다.

# 예제: 튜플의 요소들을 리스트에 추가하기
thislist = ["apple", "banana", "cherry"]
thistuple = ("kiwi", "orange")
thislist.extend(thistuple)
print(thislist)

# Remove List Items (리스트 항목 제거)
# 지정된 항목 제거 (Remove Specified Item)
# remove() 메서드는 지정된 항목을 제거합니다.

# 예제: "banana" 제거
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

# 지정된 값을 가진 항목이 두 개 이상인 경우, remove() 메서드는 첫 번째로 나타나는 항목만 제거합니다:
# 예제: 첫 번째로 나타나는 "banana" 제거
thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist)

# 지정된 인덱스 제거 (Remove Specified Index)
# pop() 메서드는 지정된 인덱스를 제거합니다.

# 예제: 두 번째 항목 제거
thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist)

# 인덱스를 지정하지 않으면, pop() 메서드는 마지막 항목을 제거합니다.
# 예제: 마지막 항목 제거
thislist = ["apple", "banana", "cherry"]
thislist.pop()
print(thislist)

# del 키워드도 지정된 인덱스를 제거합니다:
# 예제: 첫 번째 항목 제거
thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)

# del 키워드는 리스트를 완전히 삭제할 수도 있습니다.
# 예제: 전체 리스트 삭제
thislist = ["apple", "banana", "cherry"]
del thislist

# 리스트 비우기 (Clear the List)
# clear() 메서드는 리스트를 비웁니다. 리스트 자체는 여전히 남아있지만 내용은 없습니다.

# 예제: 리스트 내용 비우기
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)

# Python - Loop Lists (리스트 루프/반복)
# 네, 맞습니다! 앞에서 배운 for 문이나 while 문 같은 반복문 기법들을 리스트의 항목을 순회(loop)할 때 그대로 활용할 수 있다는 내용입니다.

# Loop Through a List (리스트 순회하기)
# for 루프를 사용하여 리스트 항목을 순회할 수 있습니다:

# 예제: 리스트의 모든 항목을 하나씩 출력하기
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

# Loop Through the Index Numbers (인덱스 번호로 순회하기)
# 인덱스 번호를 참조하여 리스트 항목을 순회할 수도 있습니다.
# range()와 len() 함수를 사용하여 적합한 반복 가능한(iterable) 객체를 만듭니다.

# 예제: 인덱스 번호를 참조하여 모든 항목 출력하기
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  print(thislist[i])
# 위 예제에서 생성된 반복 가능한 객체는 [0, 1, 2]입니다.

# Using a While Loop (While 루프 사용하기)
# while 루프를 사용하여 리스트 항목을 순회할 수 있습니다.
# len() 함수를 사용하여 리스트의 길이를 확인한 다음, 0에서 시작하여 인덱스를 참조하여 리스트 항목을วน회합니다.
# 주의: 각 반복 후에는 항상 인덱스를 1씩 늘려주어야 합니다. (무한 루프 방지)

# 예제: 모든 인덱스 번호를 순회하기 위해 while 루프를 사용하여 모든 항목 출력
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

# Looping Using List Comprehension (리스트 컴프리헨션을 사용한 루핑)
# 리스트 컴프리헨션(List Comprehension)은 리스트를 순회하는 데 가장 짧은 구문을 제공합니다.
# (이 부분은 파이썬만의 아주 독특하고 편리한 문법입니다!)

# 예제: 리스트의 모든 항목을 출력하는 단축 for 루프
thislist = ["apple", "banana", "cherry"]
[print(x) for x in thislist]

# Python - List Comprehension (리스트 컴프리헨션)
# 맞습니다! 방금 위에서 잠깐 소개되었던 '리스트 컴프리헨션'의 본격적인 내용입니다. 
# 기존 리스트의 값들을 바탕으로, 새로운 리스트를 만들거나 연산을 적용할 때 파이썬에서 아주 자주 쓰이는 강력한 기능입니다.

# List Comprehension
# 리스트 컴프리헨션은 기존 리스트의 값을 기반으로 새 리스트를 만들 때 짧은 구문을 제공합니다.

# 예제:
# 과일 리스트를 바탕으로 이름에 "a" 문자가 있는 과일만 포함하는 새 리스트를 만들고 싶다고 해봅시다.
# 리스트 컴프리헨션이 없다면 내부에 조건부 테스트가 있는 for 문을 작성해야 합니다:
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

for x in fruits:
  if "a" in x:
    newlist.append(x)
print(newlist)

# 리스트 컴프리헨션을 사용하면 한 줄의 코드만으로 이 모든 작업을 수행할 수 있습니다:
# 예제: 리스트 컴프리헨션 사용
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x for x in fruits if "a" in x]
print(newlist)

# 구문 (The Syntax)
# newlist = [expression for item in iterable if condition == True]
# 반환 값은 새 리스트이며 원래 리스트는 변경되지 않습니다.

# Condition (조건)
# 조건은 True로 평가되는 항목만 허용하는 필터와 같습니다.
# 예제: "apple"이 아닌 항목만 허용합니다:
newlist = [x for x in fruits if x != "apple"]
# x != "apple" 조건은 "apple"이 아닌 모든 요소에 대해 True를 반환하므로 새 리스트에는 "apple"을 제외한 모든 과일이 포함됩니다.

# 조건은 선택 사항이며 생략할 수 있습니다:
# 예제: if 문이 없는 경우:
newlist = [x for x in fruits]

# Iterable (반복 가능한 객체)
# 이터러블은 리스트, 튜플, 세트와 같은 모든 반복 가능한 객체일 수 있습니다.
# 예제: range() 함수를 사용하여 이터러블 만들기:
newlist = [x for x in range(10)]

# 동일한 예제, 하지만 조건이 있는 경우:
# 예제: 5보다 작은 숫자만 허용:
newlist = [x for x in range(10) if x < 5]

# Expression (표현식)
# 표현식은 반복의 현재 항목이지만, 동시에 새 리스트의 항목이 되기 전에 '변경'하거나 연산할 수 있는 결과값이기도 합니다:
# 예제: 새 리스트의 값을 대문자로 설정:
newlist = [x.upper() for x in fruits]

# 결과값을 원하는 대로 설정할 수도 있습니다:
# 예제: 새 리스트의 모든 값을 'hello'로 설정:
newlist = ['hello' for x in fruits]

# 표현식에는 조건이 포함될 수도 있습니다. 필터로서가 아니라 결과를 조작하는 방법으로서 말이죠:
# 예제: "banana" 대신 "orange" 반환 (삼항 연산자 형태의 식):
newlist = [x if x != "banana" else "orange" for x in fruits]

# Sort Lists (리스트 정렬)
# 네, 맞습니다! 원하시는 대로 리스트를 오름차순/내림차순 정렬하거나 역순으로 뒤집는 기능들입니다.

# Sort List Alphanumerically (알파벳/숫자순 정렬)
# 리스트 객체에는 기본적으로 영숫자순, 오름차순으로 정렬하는 sort() 메서드가 있습니다:

# 예제: 알파벳순으로 리스트 정렬
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

# 예제: 숫자순으로 리스트 정렬
thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

# Sort Descending (내림차순 정렬)
# 내림차순으로 정렬하려면 키워드 인수 reverse = True를 사용합니다:

# 예제: 리스트를 내림차순(알파벳 역순)으로 정렬
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)

# 예제: 리스트를 내림차순(숫자 역순)으로 정렬
thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist)

# Customize Sort Function (사용자 지정 정렬 함수)
# 키워드 인수 key = function을 사용하여 자신만의 정렬 기준(함수)을 사용자 지정할 수도 있습니다.
# 함수는 리스트를 정렬하는 데 사용될 숫자를 반환해야 합니다 (가장 낮은 숫자가 먼저 옴):

# 예제: 숫자가 50에 얼마나 가까운지를 기준으로 리스트 정렬 (abs()는 절댓값을 구하는 내장 함수)
def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)

# Case Insensitive Sort (대소문자 구분 없는 정렬)
# 기본적으로 sort() 메서드는 대소문자를 구분(case sensitive)하므로, 모든 대문자가 소문자보다 먼저 정렬됩니다:

# 예제: 대소문자를 구분하는 정렬은 예상치 못한 결과를 초래할 수 있습니다:
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist) # 출력 결과: 대문자로 시작하는 Orange, Kiwi가 먼저 나옴

# 다행히 리스트를 정렬할 때 내장 함수를 키 함수로 사용할 수 있습니다.
# 따라서 대소문자를 구분하지 않는 정렬을 원한다면 str.lower 단위를 key 함수로 사용하세요:

# 예제: 대소문자 구분 없이 리스트 정렬 수행:
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)

# Reverse Order (역순 정렬)
# 알파벳순 정렬과 관계없이 현재 요소의 순서를 그냥 반대로 뒤집고 싶다면 어떻게 해야 할까요?
# reverse() 메서드는 요소의 현재 정렬 순서를 그래도 뒤집습니다.

# 예제: 리스트 항목의 순서를 반대로 뒤집기:
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)

# Python - Copy Lists (리스트 복사)
# 네, 맞습니다! 새로운 리스트로 내용물만 똑같이 복사해 오는 방법들입니다.
# 단순히 'list2 = list1' 형식으로 복사하면 안 되는 이유가 아주 중요합니다.

# Copy a List (리스트 복사하기)
# 단순하게 list2 = list1이라고 입력하여 리스트를 복사할 수 없습니다.
# 그 이유는 list2가 오직 list1에 대한 '참조(reference)'로만 작동하기 때문에, 
# list1에서 변경한 내용이 list2에도 자동으로 적용되기 때문입니다.

# Use the copy() method (copy() 메서드 사용)
# 내장된 리스트 메서드인 copy()를 사용하여 리스트를 복사할 수 있습니다.

# 예제: copy() 메서드를 사용하여 리스트 복사본 만들기:
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

# Use the list() method (list() 인스턴스 생성자 사용)
# 복사본을 만드는 또 다른 방법은 내장 생성자인 list()를 사용하는 것입니다.

# 예제: list() 생성자를 사용하여 리스트 복사본 만들기:
thislist = ["apple", "banana", "cherry"]
mylist = list(thislist)
print(mylist)

# Use the slice Operator (슬라이스(:) 연산자 사용)
# 슬라이스 연산자(:)를 사용하여 리스트의 얕은 복사본(shallow copy)을 만들 수도 있습니다.

# 예제: : 연산자를 사용하여 리스트 복사본 만들기:
thislist = ["apple", "banana", "cherry"]
mylist = thislist[:]
print(mylist)

# Python - Join Lists (리스트 결합/합치기)
# 네, 맞습니다! 두 개 이상의 리스트를 하나로 합치거나, 다른 리스트의 항목들을 추가해서 넣는 방법들입니다.

# Example / Join two list (두 리스트 합치기)
# 가장 쉬운 방법 중 하나는 + 연산자를 사용하는 것입니다.
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)

# 두 리스트를 결합하는 또 다른 방법은 list2의 모든 항목을 list1에 하나씩 추가(appending)하는 것입니다:
# 예제: list2를 list1에 하나씩 추가(append)하기:
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

for x in list2:
  list1.append(x)
print(list1)

# 또는 한 리스트의 요소를 다른 리스트에 추가하는 목적인 extend() 메서드를 사용할 수 있습니다:
# 예제: extend() 메서드를 사용하여 list1의 끝에 list2를 추가하기:
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1)

"""
---
List Methods (리스트 메서드 모음집)
파이썬에는 리스트에 사용할 수 있는 내장 메서드(함수)들이 있습니다.

메서드     | 설명
---------|-------------------------------------------------------
append() | 리스트의 끝에 요소를 추가합니다.
clear()  | 리스트의 모든 요소를 제거합니다.
copy()   | 리스트의 복사본을 반환합니다.
count()  | 지정된 값을 가진 요소의 개수를 반환합니다.
extend() | 현재 리스트의 끝에 리스트(또는 반복 가능한 객체)의 요소를 추가합니다.
index()  | 지정된 값을 가진 첫 번째 요소의 인덱스를 반환합니다.
insert() | 지정된 위치에 요소를 추가합니다.
pop()    | 지정된 위치의 요소를 제거합니다.
remove() | 지정된 값을 가진 항목을 제거합니다.
reverse()| 리스트의 순서를 뒤집습니다.
sort()   | 리스트를 정렬합니다.
---
"""
