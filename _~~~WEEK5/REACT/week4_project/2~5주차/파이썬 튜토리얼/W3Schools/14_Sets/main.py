"""
Python Sets (세트 / 집합)
Set은 리스트, 튜플과 마찬가지로 여러 항목을 하나의 변수에 저장하는 데 사용됩니다.
가장 큰 차이점은 대괄호([])나 소괄호(()) 대신 **중괄호 `{}`**를 사용한다는 것입니다!

하지만 단순한 괄호 차이 말고도 엄청나게 중요한 3가지 특징이 있습니다:
1. Unordered (순서 없음): 순서가 없으므로 인덱스(0, 1, 2...)로 번호를 지정해서 꺼낼 수 없습니다. (매번 출력 순서가 막 바뀝니다)
2. Unchangeable (변경 불가*): 들어있는 "항목 자체"를 다른 값으로 뜯어고칠 순 없습니다. (단, 새로운 걸 통째로 추가하거나, 있는 걸 아예 빼버리는 건 가능!)
3. **Duplicates Not Allowed (중복 허용 안함)**: 가장 중요한 특징! 똑같은 걸 백 번 넣어도 하나만 남습니다. (집합의 개념)
"""

# 예제: 세트(Set) 만들기
thisset = {"apple", "banana", "cherry"}
print(thisset) 
# 참고: 실행할 때마다 출력되는 순서가 뒤죽박죽일 수 있습니다. (순서가 없기 때문)

"""
Set Items (세트 항목 특징 디테일)
- 중복된 값은 에러 없이 그냥 살포시 "무시" 됩니다.
"""

# 예제: "apple"을 두 번 넣었지만 출력해보면 한 번만 나옵니다.
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)

"""
주의할 점 (True/1, False/0 중복 처리):
파이썬 내부에서 논리값 `True`는 숫자 `1`과 완벽히 같은 값으로 취급됩니다. 
마찬가지로 `False`는 숫자 `0`과 같은 값으로 취급됩니다.
따라서 세트에 같이 넣으면 중복 발생으로 하나가 날아갑니다.
"""

# 예제: True와 1은 중복이므로 앞에 있는 True만 남고 1은 날아감
thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)

# 예제: False와 0도 중복이므로 앞에 있는 False만 0을 씹어먹고 남음
thisset = {"apple", "banana", "cherry", False, True, 0}
print(thisset)

"""
Get the Length of a Set (세트 길이 / 항목 개수 구하기)
리스트/튜플과 똑같이 len() 함수를 씁니다. 중복은 제외된 순수 개수만 나옵니다.
"""
thisset = {"apple", "banana", "cherry"}
print(len(thisset))

"""
Set Items - Data Types (데이터 타입 혼합)
세트도 항목으로 문자열, 정수, 불리언 등 어떤 데이터 타입이든 다 섞어서 담을 수 있습니다.
"""
set1 = {"abc", 34, True, 40, "male"}

"""
type() (타입 확인하기)
파이썬 관점에서 세트는 'set' 이라는 데이터 타입을 가집니다.
결과: <class 'set'>
"""
myset = {"apple", "banana", "cherry"}
print(type(myset))

"""
The set() Constructor (set 생성자)
튜플이나 리스트처럼, 생성자 함수 `set()`을 써서 자료형을 세트로 바꿀 수도 있습니다.
"""

# 주의: 괄호가 두 개 겹쳐있습니다 set((...)) -> 튜플이나 리스트를 세트로 감싼 형태
thisset = set(("apple", "banana", "cherry")) 
print(thisset)

"""
---
Access Items (세트 항목 접근하기)
세트는 '순서가 없기(Unordered)' 때문에 리스트나 튜플처럼 인덱스(`[0]`, `[1]`)를 사용해서 특정 항목을 콕 집어 꺼낼 수 없습니다.
하지만 `for` 루프를 사용해 안에 있는 항목들을 하나씩 꺼내보거나, 
`in` (혹은 `not in`) 키워드를 사용해 특정 값이 세트 안에 "존재하는지 여부"를 물어볼 수는 있습니다.
"""

# 예제: for 루프를 사용해 세트 안의 모든 값 순회하며 출력하기
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)  # 주의: 순서가 없으므로 출력될 때마다 과일 순서가 다를 수 있습니다!

# 예제: 세트 안에 "banana"가 포함되어 있는지(present) 확인하기
thisset = {"apple", "banana", "cherry"}

print("banana" in thisset)  # 결과: True

# 예제: 세트 안에 "banana"가 포함되어 있지 않은지(NOT present) 확인하기
thisset = {"apple", "banana", "cherry"}

print("banana" not in thisset)  # 결과: False


"""
---
Add Items (세트에 항목 추가하기)
세트가 한 번 만들어진 후에는 기존 항목을 '수정'할 수는 없지만, 새로운 항목을 '추가'할 수는 있습니다.
단 하나의 항목을 추가할 때는 `add()` 메서드를 사용합니다.
(리스트의 `append()`와 같은 역할을 합니다.)
"""

# 예제: add() 메서드를 사용해 세트에 "orange" 하나 추가하기
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)


"""
Add Sets (다른 세트의 항목들 통째로 추가하기)
현재 세트에 다른 세트의 모든 항목을 통째로 쏟아 붓고 싶을 때는 `update()` 메서드를 사용합니다.
(리스트의 `extend()`와 비슷한 역할입니다.)
"""

# 예제: thisset에 tropical 세트의 요소들을 통째로 붓기 (중복이 있다면 알아서 걸러집니다)
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)


"""
Add Any Iterable (어떤 반복 가능한 객체든 모두 추가 가능)
`update()` 메서드 안에는 반드시 '세트(Set)'만 넣어야 하는 것은 아닙니다!
리스트(List), 튜플(Tuple), 딕셔너리(Dictionary) 등 반복 가능한(iterable) 객체라면 무엇이든 세트 안으로 쏟아 부을 수 있습니다.
"""

# 예제: '세트' 안에 '리스트'의 요소들을 추가하기
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)


"""
---
Remove Item (세트에서 항목 제거하기)
세트에서 특정 항목을 제거할 때는 `remove()` 또는 `discard()` 메서드를 사용합니다.
"""

# 예제: remove() 메서드를 사용해 "banana" 제거하기
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset)
# 중요 포인트: 만약 세트 안에 지우려는 항목("banana")이 아예 없다면, `remove()`는 '에러(Error)'를 발생시킵니다.

# 예제: discard() 메서드를 사용해 "banana" 제거하기
thisset = {"apple", "banana", "cherry"}
thisset.discard("banana")
print(thisset)
# 중요 포인트: 지우려는 항목이 세트 안에 없더라도, `discard()`는 에러를 발생시키지 않고 그냥 무시하고 넘어갑니다!


"""
pop() 메서드로 제거하기
`pop()` 메서드를 사용해서 항목을 제거할 수도 있습니다.
하지만 매우 주의해야 할 점이 있습니다!
세트는 '순서가 없기(Unordered)' 때문에, pop()을 쓰면 "마지막 항목"이 지워지는 것이 아니라 **"어떤 항목이 지워질지 아무도 모릅니다(랜덤)."**
지워진 무작위 항목은 pop()의 결과값으로 반환됩니다.
"""

# 예제: pop() 메서드를 사용해 무작위 항목 제거하기
thisset = {"apple", "banana", "cherry"}
x = thisset.pop()  # 아무거나 하나가 튀어나오면서 제거됨
print(x)           # 지워진 항목 확인 (실행할 때마다 다를 수 있음)
print(thisset)     # 하나가 빠지고 남은 세트 확인


"""
clear() 메서드로 비우기
세트를 완전히 텅 빈 상태로 만들고 싶을 때 사용합니다.
"""
# 예제: clear() 메서드로 세트 안의 모든 항목 비우기
thisset = {"apple", "banana", "cherry"}
thisset.clear()
print(thisset)  # 출력: set() (빈 세트가 됨)


"""
del 키워드로 완전히 삭제하기
세트 변수 자체를 메모리에서 완전히 날려버리고 싶을 때 사용합니다.
"""
# 예제: del 키워드로 세트 자체를 없애버리기
thisset = {"apple", "banana", "cherry"}
del thisset
# print(thisset) # 이 줄의 주석을 풀고 실행하면 세트가 이미 삭제되었기 때문에 NameError가 발생합니다.

"""
---
Loop Items (반복문으로 세트 순회하기)
(위에서 다루었던 내용과 동일합니다!)

세트의 항목들을 하나씩 확인하고 싶을 때는 `for` 루프를 사용합니다.
단, 한 번 더 강조하지만 세트에는 인덱스 번호가 없기 때문에 `while` 루프와 `i += 1` 같은 인덱스 방식은 사용할 수 없습니다.
오직 `for x in thisset:` 같은 방식만 가능합니다!
"""

# 예제: for 루프로 세트 안의 값들 하나씩 출력하기
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)  # 주의: 출력되는 순서는 무작위입니다.

"""
---
Python - Join Sets (세트 합치기 및 집합 연산)
세트는 본질적으로 수학 시간에 배웠던 "집합(Set)"입니다.
따라서 이 파트에서는 합집합, 교집합, 차집합, 대칭차집합을 어떻게 구하는지 배웁니다.
이 기능들은 코딩 테스트에서 데이터를 강력하고 빠르게 가공할 때 핵심적으로 쓰입니다.

1. 합집합 (Union) : 두 세트의 모든 요소를 합친 새로운 세트 반환 (중복 제거)
- 메서드: `union()` 또는 `update()`
- 연산자: `|` (파이프 기호)
"""

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

# 방법 A: union() 메서드 사용 (새로운 세트 반환)
set3 = set1.union(set2) 

# 방법 B: | 연산자 사용 (같은 결과. 단, 연산자는 세트끼리만 사용 가능)
set4 = set1 | set2

print(f"합집합 (union): {set3}")


"""
2. 교집합 (Intersection) : 두 세트 양쪽에 모두 들어있는 중복 값(공통 요소)만 남기기
- 메서드: `intersection()` 또는 `intersection_update()`
- 연산자: `&` (앰퍼샌드 기호)
"""

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

# 방법 A: intersection() 메서드 사용 (공통 요소만 담긴 새 세트 반환)
set3 = set1.intersection(set2) 

# 방법 B: & 연산자 사용
set4 = set1 & set2

print(f"교집합 (intersection): {set3}")  # 출력: {'apple'}


"""
3. 차집합 (Difference) : 첫 번째 세트에는 있지만, 두 번째 세트에는 없는 항목들만 남기기 (빼기)
- 메서드: `difference()` 또는 `difference_update()`
- 연산자: `-` (마이너스 기호)
"""

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

# 예제: set1에서 set2와 겹치는 "apple"을 빼고 남은 것 반환
set3 = set1.difference(set2)
set4 = set1 - set2

print(f"차집합 (difference): {set3}") # 출력: {'cherry', 'banana'}


"""
4. 대칭차집합 (Symmetric Differences) : 두 세트의 합집합에서 '공통 요소(교집합)'만 쏙 빼고, 남은 것들만 모으기
- 메서드: `symmetric_difference()` 또는 `symmetric_difference_update()`
- 연산자: `^` (캐럿 기호)
"""

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

# 예제: 양쪽에 다 있는 "apple"만 버리고 나머지를 다 합침
set3 = set1.symmetric_difference(set2)
set4 = set1 ^ set2

print(f"대칭차집합 (symmetric_difference): {set3}") # 출력: {'google', 'banana', 'cherry', 'microsoft'}


"""
* 알아두기: `_update()` 가 붙은 메서드들의 차이점!
- `intersection()` 등: 원본은 그대로 두고 연산 결과가 담긴 "새로운 세트"를 반환합니다. `set3 = set1.intersection(set2)`
- `intersection_update()` 등: 새로운 세트를 만들지 않고, **원본 세트(set1) 자체의 내용을 연산 결과로 덮어씌워버립니다(수정합니다).** `set1.intersection_update(set2)`
"""


"""
---
Python frozenset (프로즌세트 / 얼어붙은 세트)
`frozenset`은 말 그대로 "얼어붙은" 세트입니다. **세트의 불변(Immutable) 버전**입니다.

- 일반 세트처럼 순서가 없고, 중복을 허용하지 않습니다.
- 하지만 가장 큰 차이점: **한 번 만들어지면 절대 항목을 추가(add)하거나 삭제(remove)할 수 없습니다.** (튜플과 비슷한 포지션입니다)
"""

# 예제: frozenset 생성하기 (`frozenset()` 생성자 사용)
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))  # 결과: <class 'frozenset'>

# 주의: x.add("orange") 같은 걸 시도하면 에러가 발생합니다!

"""
Frozenset Methods (프로즌세트 메서드)
프로즌세트는 안의 내용물을 수정하거나 삭제할 수 없기 때문에 `add()`, `remove()`, `update()`와 같은 메서드는 사용할 수 없습니다.
대신 내용을 바꾸지 않는, 방금 배운 "수학적 집합 연산" 기능들은 모두 사용할 수 있습니다.

메서드                  | 설명
-----------------------|-------------------------------------------
copy()                 | 복사본을 반환합니다.
difference() (-)       | 차집합을 반환합니다.
intersection() (&)     | 교집합을 반환합니다.
isdisjoint()           | 두 세트가 교집합이 하나도 없는지(완전히 안 겹치는지) 확인합니다.
issubset() (<=, <)     | 이 세트가 다른 세트의 "부분집합(쏙 들어가는지)"인지 확인합니다.
issuperset() (>=, >)   | 이 세트가 다른 세트를 "모두 품고 있는지(상위 집합)" 확인합니다.
symmetric_difference() (^)| 대칭차집합을 반환합니다.
union() (|)            | 합집합을 반환합니다.
"""

"""
---
Set Methods (세트 메서드 전체 모음집)
지금까지 배운 세트의 모든 내장 메서드와 단축 연산자 기호입니다.

메서드                          | 단축 연산자 | 설명
--------------------------------|-------------|-------------------------------------------------------
add()                           |             | 세트에 요소를 하나 추가합니다.
clear()                         |             | 세트의 모든 요소를 비웁니다 (빈 세트로 만듦).
copy()                          |             | 세트의 얕은 복사본을 반환합니다.
difference()                    | -           | 두 세트의 차집합(앞 세트에만 있는 요소들)을 반환합니다.
difference_update()             | -=          | 원본 세트에서 다른 세트와 겹치는 요소들을 직접 삭제합니다.
discard()                       |             | 세트에서 지정된 항목을 제거합니다 (항목이 없어도 에러 안 남).
intersection()                  | &           | 두 세트의 교집합(둘 다 가지고 있는 요소)을 반환합니다.
intersection_update()           | &=          | 원본 세트에 교집합 결과만 남기고 나머지는 다 버립니다.
isdisjoint()                    |             | 두 세트가 교집합이 단 하나도 없는지 검사합니다 (True/False).
issubset()                      | <=          | 이 세트가 다른 세트에 완전히 포함되는지(부분집합) 검사합니다.
                                | <           | 이 세트가 다른 세트의 '진부분집합(같지 않고 더 작은 부분집합)'인지 검사.
issuperset()                    | >=          | 이 세트가 다른 세트를 완전히 품고 있는지(상위집합) 검사합니다.
                                | >           | 이 세트가 다른 세트를 포함하는 '진상위집합'인지 검사.
pop()                           |             | 세트에서 무작위로 아무 항목이나 하나 제거하고 그 값을 반환합니다.
remove()                        |             | 지정된 요소를 제거합니다 (항목이 없으면 에러 발생!).
symmetric_difference()          | ^           | 두 세트의 대칭차집합(서로 안 겹치는 것들만)을 반환합니다.
symmetric_difference_update()   | ^=          | 원본 세트를 대칭차집합 결과로 덮어씌웁니다.
union()                         | |           | 두 세트를 합친 합집합을 반환합니다.
update()                        | |=          | 현재 세트에 다른 세트(또는 리스트 등)를 통째로 부어 업데이트합니다.
---
"""








