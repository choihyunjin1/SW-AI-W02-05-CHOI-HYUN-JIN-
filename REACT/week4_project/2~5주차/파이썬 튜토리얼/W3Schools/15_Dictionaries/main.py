"""
Python Dictionaries (딕셔너리 / 사전)
파이썬의 자료구조 끝판왕입니다! (알고리즘 문제 풀 때 가장 핵심적인 '해시맵(Hash Map)' 역할을 합니다.)

실제 우리가 아는 "사전(Dictionary)"을 생각해보세요.
사전에서 "apple"이라는 단어(Key)를 찾으면, 그 옆에 "사과"라는 뜻(Value)이 적혀있죠?
이처럼 딕셔너리는 데이터를 항상 **"키(Key) : 값(Value)"** 이라는 한 쌍(Pair)으로 저장합니다.

- 괄호: 세트처럼 중괄호 `{}`를 사용하지만, 안에 들어가는 모양이 `키: 값` 형태입니다.
- 특징: 
  1. Ordered (순서가 있음* - Python 3.7부터)
  2. Changeable (수정 가능)
  3. **Duplicates Not Allowed (중복 허용 안됨!)**
"""

# 예제: 딕셔너리를 생성하고 출력하기
thisdict = {
  "brand": "Ford",     # "brand"라는 키를 찾으면 "Ford"라는 값이 나온다.
  "model": "Mustang",  # "model"이라는 키를 찾으면 "Mustang"이 나온다.
  "year": 1964         # "year"라는 키를 찾으면 1964가 나온다.
}
print(thisdict)

"""
Dictionary Items (딕셔너리 항목의 특징)
딕셔너리의 데이터는 인덱스 번호(`[0]`, `[1]`)가 아니라, **"키(Key)의 이름"**을 사용해서 불러옵니다!
"""

# 예제: "brand"라는 키를 불러와서 그 값("Ford")을 출력하기
print(thisdict["brand"])

"""
Ordered vs Unordered (순서가 있나요?)
- Python 3.7 버전부터는: 딕셔너리에 데이터를 넣은 순서가 그대로 유지됩니다. (Ordered)
- Python 3.6 이하 구버전에서는: 세트처럼 순서가 뒤죽박죽이었습니다.
(*알고리즘 문제를 풀 때는 항상 최신 버전 기준이므로 순서가 유지된다고 생각하시면 됩니다.)

Changeable (수정 가능)
딕셔너리가 만들어진 후에도 내용을 추가, 삭제, 수정하는 것이 아주 자유롭습니다.

Duplicates Not Allowed (중복 불가!)
딕셔너리에서 **"키(Key)"는 절대 중복될 수 없습니다.** (값(Value)은 중복돼도 상관없음)
만약 똑같은 키를 두 번 쓰면 어떻게 될까요? 가장 마지막에 쓴 값으로 덮어쓰기(Overwrite) 됩니다!
"""

# 예제: "year"라는 키를 두 번 썼을 때
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020  # 동일한 키("year")를 또 쓰면 기존 1964를 2020이 덮어버림!
}
print(thisdict)  # "year"는 2020 하나만 남음

"""
Dictionary Length (데이터 개수 구하기)
len() 함수를 쓰면 '키:값 쌍'이 총 몇 개 들어있는지 알려줍니다.
"""
print(len(thisdict))

"""
Dictionary Items - Data Types (어떤 데이터가 들어갈까?)
값(Value) 자리에는 문자열, 정수, 불리언은 물론이고 리스트, 튜플 등 **파이썬의 모든 데이터 타입**을 다 넣을 수 있습니다!
"""

# 예제: 값 자리에 다양한 자료형(불리언, 리스트 등)을 담은 딕셔너리
thisdict2 = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]  # 값으로 '리스트'를 통째로 넣음
}

print(type(thisdict2))  # 결과: <class 'dict'>

"""
The dict() Constructor (dict 생성자)
dict() 함수를 사용해서 딕셔너리를 만들 수도 있습니다.
(주의: 이때는 키 이름을 적을 때 따옴표("")를 생략해야 하고, 콜론(:) 대신 등호(=)를 씁니다.)
"""
thisdict3 = dict(name="John", age=36, country="Norway")
print(thisdict3)


"""
💡 [요약] 파이썬의 4대 컬렉션(자료구조) 비교
이 4가지를 정확히 구분하는 것이 파이썬의 핵심이자 첫걸음입니다!

1. List (리스트 `[]`): 순서O, 수정O, 중복O (가장 흔하게 쓰는 배열)
2. Tuple (튜플 `()`): 순서O, 수정X, 중복O (절대 안 변하는 리스트)
3. Set (세트 `{}`): 순서X, 수정X(추가는 가능), 중복X (중복 제거기, 집합)
4. Dictionary (딕셔너리 `{키:값}`): 순서O, 수정O, 중복X (키를 통해 값을 찾는 사전)
"""

"""
---
Accessing Items (항목 접근하기)
딕셔너리의 값을 가져오려면, 대괄호 `[]` 안에 "키(Key) 이름"을 넘겨주면 됩니다.
"""

# 예제: "model" 키의 값을 가져오기
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]  # Mustang 반환
print(x)

# get() 메서드 사용하기
# 대괄호를 쓰는 것과 완전히 똑같은 결과를 내는 .get() 메서드도 있습니다.
x = thisdict.get("model")


"""
Get Keys (모든 키(이름표)만 싹 모아서 뽑아오기)
`keys()` 메서드를 사용하면 딕셔너리 안에 있는 "키"들만 모아서 리스트(View 객체) 형태로 돌려줍니다.
특징: 원본 딕셔너리에 뭔가 추가/수정되면 이 뽑아둔 리스트도 실시간으로 알아서 업데이트됩니다!
"""

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}
x = car.keys()
print(x) # 출력: dict_keys(['brand', 'model', 'year'])

car["color"] = "white" # 원본에 새로운 키-값 추가!
print(x) # 출력: dict_keys(['brand', 'model', 'year', 'color']) ⬅️ x를 다시 안 뽑았는데도 알아서 "color"가 추가되어 있음!


"""
Get Values (모든 값(내용물)만 싹 모아서 뽑아오기)
`values()` 메서드를 사용하면 딕셔너리 안에 있는 "값"들만 모아서 돌려줍니다.
"""

x = car.values()
print(x) # 출력: dict_values(['Ford', 'Mustang', 1964, 'white'])

car["year"] = 2020 # 값을 변경하면
print(x) # 실시간으로 반영되어 2020으로 보임


"""
Get Items (키와 값을 쌍(Tuple)으로 묶어서 모두 뽑아오기) ★가장 많이 씁니다★
`items()` 메서드를 사용하면 `(키, 값)` 형태의 튜플들이 들어있는 리스트를 돌려줍니다.
나중에 for 반복문을 돌릴 때 "키와 값을 동시에" 꺼내려면 무조건 이걸 씁니다.
"""

# 예제: items() 사용
x = car.items()
print(x) # 출력: dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 2020), ('color', 'white')])


"""
Check if Key Exists (특정 키가 존재하는지 확인하기)
`in` 키워드를 사용하면 해당 "키(Key)"가 딕셔너리에 존재하는지 검사할 수 있습니다.
(주의: 이건 '값(Value)'이 있는지를 검사하는 게 아니라 '이름표(Key)'가 있는지를 검사하는 겁니다!)
"""

# 예제: "model"이라는 키가 이 딕셔너리에 있나요?
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
if "model" in thisdict:
  print("Yes, 'model' key가 존재합니다.")


"""
---
Change Values (딕셔너리 값 변경하기)
이미 존재하는 딕셔너리의 값을 바꾸고 싶다면, 대괄호 `[]` 안에 원하는 키를 넣고 새로운 값을 할당(`=`)하면 됩니다.
"""

# 예제: "year"의 값을 1964에서 2018로 변경하기
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["year"] = 2018  # "year" 키가 이미 있으니까 값을 2018로 덮어씌움!
print(thisdict)


"""
Update Dictionary (update() 메서드로 업데이트하기)
`update()` 메서드를 사용하면, 다른 딕셔너리 모양의 데이터 `{키: 값}`을 통째로 넘겨서 값을 업데이트할 수 있습니다.
만약 넘겨준 키가 기존에 있던 것이라면 값이 "수정"되고, 없던 것이라면 새로 "추가"됩니다.
"""

# 예제: update() 메서드를 사용하여 "year"를 2020으로 업데이트하기
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

# 주의: 소괄호 안에 중괄호를 넣어서 딕셔너리 형태로 넘겨줍니다.
thisdict.update({"year": 2020})
print(thisdict)


"""
Add Dictionary Items (딕셔너리 항목 추가하기)
Adding Items (항목 추가하기)
새로운 인덱스 키를 사용하고 거기에 값을 할당하면 딕셔너리에 항목이 추가됩니다.
(기존에 없던 키라면 "추가"되고, 있던 키라면 "수정"이 됩니다.)
"""

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["color"] = "red" # "color" 키가 없었으므로 새로 추가됨
print(thisdict)


"""
Update Dictionary (update()로 딕셔너리 추가/업데이트하기)
`update()` 메서드를 사용하면 주어진 매개변수 항목들로 딕셔너리가 업데이트됩니다. 
만약 해당 항목이 존재하지 않는다면 새로 추가됩니다.
매개변수는 딕셔너리이거나 키:값 쌍인 반복 가능한 객체여야 합니다.
"""

# 예제: update() 메서드를 사용하여 color 항목을 추가하기
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"color": "red"})
print(thisdict)


"""
Removing Items (항목 제거하기)
딕셔너리에서 항목을 제거하는 데는 몇 가지 메서드가 있습니다:
"""

# 1. pop() 메서드: 지정된 키 이름을 가진 항목을 제거합니다.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.pop("model") 
print(thisdict)


# 2. popitem() 메서드: 마지막으로 삽입된 항목을 제거합니다!
# (버전 3.7 이전에는 무작위 항목이 제거되었습니다)
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.popitem()
print(thisdict)


# 3. del 키워드: 지정된 키 이름을 가진 항목을 제거합니다.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
del thisdict["model"]
print(thisdict)

# 주의: del 키워드는 딕셔너리 변수 자체를 완전히 삭제할 수도 있습니다.
# del thisdict  # <- 이거 하면 앞으로 thisdict를 쓸 수 없게 됩니다.


# 4. clear() 메서드: 딕셔너리를 통째로 비워버립니다.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.clear()
print(thisdict) # 출력: {} (빈 딕셔너리)


"""
Loop Through a Dictionary (딕셔너리 반복문 돌리기)
for 루프를 사용해서 딕셔너리를 반복할 수 있습니다.
그냥 반복시키면 기본적으로 반환되는 값은 딕셔너리의 "키(Keys)"들입니다. 
하지만 "값(Values)"들을 반환시키는 메서드도 있습니다.
"""

thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# 예제 1: 딕셔너리의 모든 '키' 이름들을 하나씩 출력하기
print("--- 키 출력 ---")
for x in thisdict:
  print(x)

# 예제 2: 딕셔너리의 모든 '값'들을 하나씩 출력하기
print("--- 값 출력 (대괄호 접근) ---")
for x in thisdict:
  print(thisdict[x])


# 예제 3: values() 메서드를 사용하여 값 반환하기
print("--- values()로 값 출력 ---")
for x in thisdict.values():
  print(x)


# 예제 4: keys() 메서드를 사용하여 키 반환하기
print("--- keys()로 키 출력 ---")
for x in thisdict.keys():
  print(x)


# 예제 5: items() 메서드를 사용하여 키와 값을 동시에 반복하기 ★가장 많이 씁니다★
print("--- items()로 키, 값 같이 출력 ---")
for x, y in thisdict.items():
  print(f"{x}: {y}")


"""
Copy a Dictionary (딕셔너리 복사하기)
`dict2 = dict1` 처럼 대입해서 딕셔너리를 복사할 수는 없습니다.
왜냐하면 물리적 복사가 아니라 "참조"만 하기 때문에, dict1을 바꾸면 dict2도 같이 바뀌어버립니다.
복사본을 만들려면 파이썬 내장 메서드인 `.copy()` 또는 `dict()` 함수를 써야 합니다.
"""

# 예제: copy() 메서드를 사용해 복사
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
print(mydict)


# 예제: dict() 함수를 사용해 복사
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = dict(thisdict)
print(mydict)


"""
Python - Nested Dictionaries (중첩 딕셔너리 - 딕셔너리 안에 딕셔너리)
딕셔너리는 내부에 또 다른 딕셔너리를 담을 수 있습니다. 이를 "중첩 딕셔너리"라고 부릅니다.
"""

# 예제 1: 3개의 딕셔너리를 담은 하나의 큰 딕셔너리 생성하기
myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}
print(myfamily)


# 예제 2: 각각 딕셔너리를 3개 만든 다음, 그걸 모아서 새 딕셔너리 만들기
child1 = {
  "name" : "Emil",
  "year" : 2004
}
child2 = {
  "name" : "Tobias",
  "year" : 2007
}
child3 = {
  "name" : "Linus",
  "year" : 2011
}

myfamily = {
  "child1" : child1,
  "child2" : child2,
  "child3" : child3
}
print(myfamily)


"""
Access Items in Nested Dictionaries (중첩 딕셔너리 항목 접근)
중첩된 딕셔너리의 항목에 접근하려면 바깥쪽부터 안쪽으로 차례로 대괄호(키 이름)를 연결하면 됩니다.
"""

# 예제: child2(두 번째 아이)의 name(이름) 출력하기
print(myfamily["child2"]["name"]) # 출력: Tobias


"""
Loop Through Nested Dictionaries (중첩 딕셔너리 반복문)
items() 메서드를 통해 바깥 딕셔너리와 안쪽 딕셔너리의 키/값을 다 뽑아볼 수 있습니다.
"""

# 예제: 모든 중첩 딕셔너리 내용 출력하기
for x, obj in myfamily.items():
  print(x) # 바깥 키 (ex: child1)
  
  for y in obj:
    print(y + ':', obj[y]) # 안쪽 딕셔너리 요소 하나씩 (ex: name: Emil)


"""
Dictionary Methods (딕셔너리 메서드 정리)

- clear() : 딕셔너리의 모든 요소를 제거합니다.
- copy() : 딕셔너리의 복사본을 반환합니다.
- fromkeys() : 지정된 키들과 값을 써서 새 딕셔너리를 반환합니다.
- get() : 지정된 키의 값을 반환합니다. ([키] 접근 시 없는 키면 오류나지만 이거 쓰면 None 나옵니다)
- items() : 각 '키: 값' 쌍이 들어있는 리스트(뷰)를 반환합니다.
- keys() : 딕셔너리의 모든 키가 들어있는 리스트(뷰)를 반환합니다.
- pop() : 지정된 키를 가진 요소를 제거합니다.
- popitem() : 가장 마지막에 삽입된 키-값 쌍을 제거합니다.
- setdefault() : 지정된 키의 값을 반환합니다. 단, 키가 없다면 주어진 값으로 키를 새로 만듭니다.
- update() : 주어진 항목 또는 지정된 키-값 쌍으로 딕셔너리를 업데이트합니다.
- values() : 딕셔너리의 모든 값들이 들어있는 리스트(뷰)를 반환합니다.
"""


