"""
Python Arrays (파이썬 배열)
참고: 파이썬은 내장 배열(Array)을 지원하지 않지만, 대신 파이썬 리스트(List)를 사용할 수 있습니다.

배열 (Arrays)
참고: 이 페이지에서는 LISTS를 ARRAYS처럼 사용하는 방법을 보여줍니다. 하지만 파이썬에서 실제 배열을 다루려면 NumPy와 같은 라이브러리를 임포트(import)해야 합니다.

배열은 단일 변수에 여러 값을 저장하는 데 사용됩니다.
"""

print("--- 배열 생성하기 ---")
# 예제: 차 이름을 포함하는 배열(리스트) 생성하기
cars = ["Ford", "Volvo", "BMW"]
print(cars)


"""
배열이란? (What is an Array?)
배열은 한 번에 둘 이상의 값을 보유할 수 있는 특수 변수입니다.

항목 목록(예: 차 이름 목록)이 있는 경우, 단일 변수에 각각 저장하면 다음과 같을 수 있습니다.
car1 = "Ford"
car2 = "Volvo"
car3 = "BMW"

하지만 특정 차를 찾기 위해 루프를 돌리고 싶다면 어떻게 해야 할까요? 차가 3대가 아니라 300대라면 어떻게 해야 할까요?
해결책은 배열입니다!
배열은 단일 이름으로 많은 값을 보유할 수 있으며 인덱스 번호를 참조하여 값에 액세스할 수 있습니다.


배열의 요소에 접근하기 (Access the Elements of an Array)
인덱스 번호를 참조하여 배열 요소에 접근합니다.
"""

print("\n--- 배열 요소에 접근 및 수정 ---")
# 예제: 첫 번째 배열 항목의 값 가져오기
x = cars[0]
print("cars[0]:", x)

# 예제: 첫 번째 배열 항목의 값 수정하기
cars[0] = "Toyota"
print("수정된 cars:", cars)


"""
배열의 길이 (The Length of an Array)
배열의 길이(배열의 요소 수)를 반환하려면 len() 메서드를 사용합니다.
"""

print("\n--- 배열의 길이 ---")
# 예제: cars 배열의 요소 수 반환하기
x = len(cars)
print("배열 cars의 길이:", x)
# 참고: 배열의 길이는 항상 가장 높은 배열 인덱스보다 1 더 큽니다.


"""
배열 요소 반복하기 (Looping Array Elements)
for in 루프를 사용하여 배열의 모든 요소를 반복할 수 있습니다.
"""

print("\n--- 배열 요소 반복하기 ---")
# 예제: cars 배열의 각 항목 프린트하기
for x in cars:
    print(x)


"""
배열 요소 추가하기 (Adding Array Elements)
append() 메서드를 사용하여 배열에 요소를 추가할 수 있습니다.
"""

print("\n--- 배열 요소 추가 ---")
# 예제: cars 배열에 요소 하나 더 추가하기
cars.append("Honda")
print("추가 후 cars:", cars)


"""
배열 요소 제거하기 (Removing Array Elements)
pop() 메서드를 사용하여 배열에서 요소를 제거할 수 있습니다.
"""

print("\n--- 배열 요소 제거 (pop) ---")
# 예제: cars 배열의 두 번째 요소 삭제하기
cars.pop(1)
print("pop(1) 후 cars:", cars)

"""
remove() 메서드를 사용하여 배열에서 요소를 제거할 수도 있습니다.
"""

print("\n--- 배열 요소 제거 (remove) ---")
# 예제: "Honda" 값을 가진 요소 삭제하기 ("Volvo"는 pop으로 지워졌을 수 있으니 Honda로 대체)
cars.remove("Honda")
print("remove('Honda') 후 cars:", cars)
# 참고: 리스트의 remove() 메서드는 지정된 값의 첫 번째로 나타나는 일치 항목만 제거합니다.


"""
배열 메서드 (Array Methods)
파이썬에는 리스트/배열에 사용할 수 있는 내장 메서드 세트가 있습니다.

append()  : 리스트 끝에 요소를 추가합니다.
clear()   : 리스트에서 모든 요소를 제거합니다.
copy()    : 리스트의 복사본을 반환합니다.
count()   : 지정된 값과 일치하는 요소의 개수를 반환합니다.
extend()  : 현재 리스트의 끝에 리스트(또는 임의의 iterable)의 요소를 추가합니다.
index()   : 지정된 값이 있는 첫 번째 요소의 인덱스를 반환합니다.
insert()  : 지정된 위치에 요소를 추가합니다.
pop()     : 지정된 위치에 있는 요소를 제거합니다.
remove()  : 지정된 값을 가진 첫 번째 항목을 제거합니다.
reverse() : 리스트의 순서를 뒤집습니다.
sort()    : 리스트를 정렬합니다.
"""