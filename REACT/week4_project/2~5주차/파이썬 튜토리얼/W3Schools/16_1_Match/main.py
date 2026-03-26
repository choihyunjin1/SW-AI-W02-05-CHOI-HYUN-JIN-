"""
Python Match Statement (파이썬 Match 문)
(이 기능은 파이썬 3.10 버전부터 새롭게 추가되었습니다!)
수많은 if..elif..else 문을 작성하는 대신, match 문을 사용할 수 있습니다.
다른 언어의 'switch-case' 문과 유사하게 동작합니다.

[작동 방식]
1. match 표현식이 한 번만 평가됩니다.
2. 표현식의 값이 각 case의 값과 비교됩니다.
3. 일치하는 항목이 있으면 해당 코드 블록이 실행됩니다.
"""

# 예제 1: 요일 번호를 사용해 요일 이름 출력하기
day = 4
print("--- [예제 1] 기본 Match 문 ---")
match day:
  case 1:
    print("월요일")
  case 2:
    print("화요일")
  case 3:
    print("수요일")
  case 4:
    print("목요일")
  case 5:
    print("금요일")
  case 6:
    print("토요일")
  case 7:
    print("일요일")

print("\n")


"""
Default Value (기본값 설정)
다른 매칭되는 case가 없을 때 실행할 코드 블록을 원한다면 
마지막 case 값으로 언더스코어(_) 문자를 사용합니다. 
(이것은 if-else 문의 'else'와 완전히 동일한 역할을 합니다)
"""

# 예제 2: 일치하는 것이 없을 때의 기본값 처리
day = 4
print("--- [예제 2] Default Value (_) 처리 ---")
match day:
  case 6:
    print("오늘은 토요일입니다.")
  case 7:
    print("오늘은 일요일입니다.")
  case _:
    print("주말이 오기를 기다리고 있습니다. (평일)")


print("\n")


"""
Combine Values (값 결합하기 - OR 역할)
파이프 문자(|)를 'OR' 연산자처럼 사용하여, 
하나의 case 문에서 여러 값을 동시에 검사할 수 있습니다.
"""

# 예제 3: 여러 case 값을 한 번에 묶어서 매칭하기
day = 4
print("--- [예제 3] 값 결합(| 연산자) ---")
match day:
  case 1 | 2 | 3 | 4 | 5:
    print("오늘은 평일입니다.")
  case 6 | 7:
    print("나는 주말을 사랑합니다!")


print("\n")


"""
If Statements as Guards (가드로써의 If 문)
case 평가 시 추가적인 조건 검사로 if 문을 뒤에 붙일 수 있습니다.
이를 파이썬에서는 '가드(Guard)' 조건이라고 부릅니다.
"""

# 예제 4: 조건에 따라 더 디테일하게 필터링하기
month = 5
day = 4
print("--- [예제 4] If Statements as Guards ---")
match day:
  case 1 | 2 | 3 | 4 | 5 if month == 4:
    print("4월의 어떤 평일입니다.")
  case 1 | 2 | 3 | 4 | 5 if month == 5:
    print("5월의 어떤 평일입니다.")
  case _:
    print("일치하는 항목이 없습니다.")
