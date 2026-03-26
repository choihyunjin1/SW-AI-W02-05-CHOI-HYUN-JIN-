"""
Python Modules (파이썬 모듈)

모듈이란 무엇인가요? (What is a Module?)
모듈을 코드 라이브러리(code library)와 같다고 생각하시면 됩니다.
이는 응용 프로그램에 포함하려는 함수(또는 변수 등)들의 집합이 포함된 파일입니다.

모듈 생성하기 (Create a Module)
모듈을 생성하려면 원하는 코드를 `.py` 파일 확장자를 가진 파일로 저장하기만 하면 됩니다.
이 폴더에 `mymodule.py`라는 파일을 미리 생성해 두었습니다!
(mymodule.py 내용: greeting() 함수와 person1 딕셔너리가 들어있습니다.)

모듈 사용하기 (Use a Module)
이제 `import` 문을 사용하여 우리가 만든 모듈을 사용할 수 있습니다.
"""

print("--- 모듈 사용하기 ---")
# 예제: mymodule이라는 이름의 모듈을 가져오고(import) greeting 함수 호출하기
import mymodule

mymodule.greeting("Jonathan")
# 참고: 모듈에 있는 함수를 사용할 때는 구문: module_name.function_name 을 사용하세요.


"""
모듈 내 변수 (Variables in Module)
모듈에는 앞에서 설명한 대로 함수뿐만 아니라 모든 유형(배열, 딕셔너리, 객체 등)의 변수를 포함시킬 수 있습니다.
mymodule.py 파일에는 "person1" 이라는 딕셔너리 정보가 이미 들어있습니다.
"""

print("\n--- 모듈 내 변수 접근하기 ---")
# 예제: mymodule 모듈에서 person1 딕셔너리에 접근하기
import mymodule

a = mymodule.person1["age"]
print("person1의 age:", a)


"""
모듈 이름 짓기 (Naming a Module)
모듈 파일의 이름은 원하는 대로 지을 수 있지만, 반드시 .py 파일 확장자를 가져야 합니다.

모듈 이름 바꾸기 (Re-naming a Module)
모듈을 가져올 때 `as` 키워드를 사용하여 별칭(alias)을 만들 수 있습니다.
"""

print("\n--- 모듈 이름 바꾸기 (별칭 생성) ---")
# 예제: mymodule의 별칭을 mx로 생성하기
import mymodule as mx

a = mx.person1["age"]
print("mx.person1['age']:", a)


"""
내장 모듈 (Built-in Modules)
파이썬에는 여러 기본 파이썬 내장 모듈이 있으며, 원할 때마다 가져올 수(import) 있습니다.
"""

print("\n--- 기본 내장 모듈 사용하기 ---")
# 예제: platform 모듈을 가져오고 사용하기
import platform

x = platform.system()
print("현재 실행 중인 플랫폼 시스템:", x)


"""
dir() 함수 사용하기 (Using the dir() Function)
모듈 내에 있는 모든 함수 이름(또는 변수 이름)을 나열하는 내장 함수인 dir() 함수가 있습니다.
"""

print("\n--- dir() 함수 사용하기 ---")
# 예제: platform 모듈에 속한 모든 정의된 이름 목록을 나열하기
import platform

x = dir(platform)
# 출력이 너무 길어질 수 있으므로, 결과 리스트의 처음 5개 항목만 출력해보겠습니다.
print("platform 모듈의 함수 및 변수 목록 (일부):", x[:5], "...")
# 참고: dir() 함수는 파이썬 기본 모듈뿐만 아니라 여러분이 직접 만든 모든 모듈에도 사용할 수 있습니다.


"""
모듈에서 가져오기 (Import From Module)
`from` 키워드를 사용하여 모듈에서 오직 일부부만 선택적으로 가져올 수 있습니다.
mymodule 에는 greeting 함수와 person1 딕셔너리가 들어있습니다.
"""

print("\n--- 모듈에서 일부분만 가져오기 (from ... import ...) ---")
# 예제: 모듈에서 person1 딕셔너리만 가져오기
from mymodule import person1

print('person1["age"]:', person1["age"])
# 참고: 'from' 키워드를 사용하여 모듈을 들여올 때는 모듈 이름을 사용할 필요가 없습니다. 
# 구문 예: 'mymodule.person1' 대신 그냥 'person1'을 사용합니다.

