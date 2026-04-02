"""
Python Iterators (파이썬 이터레이터)

파이썬 이터레이터
이터레이터(Iterator)는 셀 수 있는 개수의 값을 포함하는 객체입니다.
이터레이터는 반복할 수 있는(iterable) 객체이며, 이는 모든 값을 순회할 수 있음을 의미합니다.
기술적으로 파이썬에서 이터레이터는 __iter__() 및 __next__() 메서드로 구성된 이터레이터 프로토콜(iterator protocol)을 구현하는 객체입니다.

Iterator vs Iterable (이터레이터 vs 이터러블)
리스트, 튜플, 딕셔너리, 세트는 모두 반복 가능한(iterable) 객체입니다. 이것들은 모두 이터레이터를 얻을 수 있는 이터러블 컨테이너입니다.
이 모든 객체는 이터레이터를 얻는 데 사용되는 iter() 메서드를 가지고 있습니다.
"""

print("--- 튜플에서 이터레이터 반환 ---")
# 예제: 튜플에서 이터레이터를 반환하고 각 값을 출력하기
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


"""
문자열조차도 이터러블 객체이며 이터레이터를 반환할 수 있습니다.
"""

print("\n--- 문자열에서 이터레이터 반환 ---")
# 예제: 문자열은 문자의 시퀀스를 포함하는 이터러블 객체입니다.
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))


"""
이터레이터 반복하기 (Looping Through an Iterator)
for 루프를 사용하여 이터러블 객체를 순회할 수도 있습니다.
"""

print("\n--- 이터러블 객체 반복 ---")
# 예제: 튜플의 값 순회하기
mytuple = ("apple", "banana", "cherry")
for x in mytuple:
    print(x)


# 예제: 문자열의 문자 순회하기
print("--- 문자열 문자 반복 ---")
mystr = "banana"
for x in mystr:
    print(x)

# for 루프는 실제로 이터레이터 객체를 생성하고 각 루프마다 next() 메서드를 실행합니다.


"""
이터레이터 만들기 (Create an Iterator)
객체/클래스를 이터레이터로 만들려면 객체에 __iter__() 및 __next__() 메서드를 구현해야 합니다.
Python 클래스/객체 챔터에서 배우게 되겠지만, 모든 클래스에는 객체가 생성될 때 초기화 작업을 할 수 있게 해주는 __init__()이라는 함수가 있습니다.
__iter__() 메서드도 비슷하게 동작하며, 연산(초기화 등)을 수행할 수 있지만 항상 이터레이터 객체 자체를 반환해야 합니다.
__next__() 메서드 역시 연산을 수행할 수 있으며, 시퀀스의 다음 항목을 반환해야 합니다.
"""

print("\n--- 커스텀 이터레이터 예제 (MyNumbers) ---")
# 예제: 1부터 시작하여 시퀀스마다 1씩 증가하는 숫자들을 반환하는 이터레이터 생성 (1, 2, 3, 4, 5 등을 반환)
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))


"""
StopIteration (반복 중지)
만약 충분한 next() 문이 있거나 for 루프에서 사용된다면, 위 예제는 영원히 계속될 것입니다.
반복이 영원히 계속되는 것을 막기 위해 StopIteration 문을 사용할 수 있습니다.
__next__() 메서드 내에, 반복이 지정된 횟수만큼 수행되면 오류를 발생시켜 종료하는 조건을 추가할 수 있습니다.
"""

print("\n--- StopIteration 예제 ---")
# 예제: 20번의 반복 후 정지 (1부터 20까지만 출력)
class MyNumbersWithStop:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration

myclass_stop = MyNumbersWithStop()
myiter_stop = iter(myclass_stop)

for x in myiter_stop:
    print(x, end=' ')
print() # 마지막 줄바꿈

