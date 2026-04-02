"""
Python Conditions and If statements (파이썬 조건문과 If문)
파이썬은 수학의 일반적인 논리 조건을 지원합니다:
- 같음 (Equals): a == b
- 같지 않음 (Not Equals): a != b
- 미만 (Less than): a < b
- 이하 (Less than or equal to): a <= b
- 초과 (Greater than): a > b
- 이상 (Greater than or equal to): a >= b

if 키워드를 사용해 "if 문"을 작성합니다.
만약 조건이 참(True)이면, if 문 안의 코드 블록이 실행됩니다!
거짓(False)이면 건너뜁니다.
"""

# 1. If문 기본 예제
a = 33
b = 200
if b > a:
  print("b가 a보다 큽니다")

print("-" * 30)

"""
Indentation (들여쓰기)
파이썬은 코드의 범위를 지정하기 위해 들여쓰기(줄 시작 부분의 공백)에 의존합니다.
(다른 프로그래밍 언어들은 종종 이 목적으로 중괄호 {}를 사용합니다)
★ 들여쓰기는 스페이스나 탭을 사용할 수 있지만, 같은 코드 블록 내에서는 동일한 양의 들여쓰기를 사용해야 합니다.
"""

age = 20

# if 블록 안의 다중 식 (들여쓰기 수준이 모두 같아야 합니다)
if age >= 18:
  print("당신은 성인입니다.")
  print("투표할 수 있습니다.")
  print("모든 법적 권리를 갖습니다.")

print("-" * 30)

"""
The Elif Keyword (Elif 키워드)
elif 키워드는 파이썬에서 "이전 조건이 참이 아니었다면, 이번 조건을 시도해봐라"라는 뜻입니다.
순서대로 확인하다가 참인 조건이 나오면 그 블록을 실행하고, 나머지 조건들은 전부 테스트하지 않고 건너뜁니다!
"""

score = 75

if score >= 90:
  print("성적: A")
elif score >= 80:
  print("성적: B")
elif score >= 70:
  print("성적: C")
elif score >= 60:
  print("성적: D")
# 점수가 75이므로, 위에서부터 확인하다가 'score >= 70' 조건이 참이 되어 "성적: C"가 출력됩니다.

print("-" * 30)


"""
The Else Keyword (Else 키워드)
else 키워드는 이전의 모든 조건(if 또는 elif)에 해당하지 않는 '나머지 모든 경우'를 잡아냅니다.
마치 "모두 아니면 이거 실행해" 라는 안전망(fallback)과 같습니다. (※ 무조건 마지막에 와야 합니다)
"""

temperature = 22

if temperature > 30:
  print("밖에 매우 덥네요!")
elif temperature > 20:
  print("따뜻한 날씨입니다.")
elif temperature > 10:
  print("선선하네요.")
else:
  print("밖에 춥습니다!")

print("-" * 30)


"""
Short Hand If (짧은 if 문 / 한 줄 if 문)
실행할 구문이 단 하나뿐이라면, if 문과 같은 줄에 바로 작성할 수 있습니다.
"""

# 한 줄 if 문 (조건식 뒤에 콜론(:)은 여전히 필요합니다)
a = 5
b = 2
if a > b: print("a가 b보다 큽니다! (한 줄)")


"""
Short Hand If ... Else (조건부 표현식 / 삼항 연산자)
if용으로 한 줄, else용으로 한 줄만 실행할 거라면 코드를 단 한 줄로 줄일 수 있습니다.
문법: [참일 때 값] if [조건식] else [거짓일 때 값]
"""

# 값을 반환하여 출력하기
a = 2
b = 330
print("A가 큼") if a > b else print("B가 크거나 같음")

# 조건에 따라 변수에 값 할당하기 (아주 실용적이고 많이 쓰입니다!)
x = 15
y = 20
max_value = x if x > y else y
print("두 수 중 최댓값:", max_value)

print("-" * 30)


"""
Python Logical Operators (논리 연산자)
논리 연산자는 조건문을 여러 개 결합할 때 사용합니다:
1. and : 양쪽 조건이 모두 참(True)이어야 전체가 참이 됩니다.
2. or  : 양쪽 중 하나라도 참(True)이면 전체가 참이 됩니다.
3. not : 결과의 반대를 반환합니다 (참이면 거짓, 거짓이면 참).

※ 파이썬의 연산 우선순위는 `not` -> `and` -> `or` 순서입니다.
※ 헷갈릴 때는 조건식 겉에 소괄호 `()`를 쳐서 묶어주는 것이 가장 좋습니다.
"""

age = 25
is_student = False
has_discount_code = True

# 괄호를 이용해 복잡한 조건식을 만들 수 있습니다.
# (나이가 18미만/65초과 거나) -> 거짓
# (학생이 아니거나) -> not is_student = 참! (여기가 성립해서 and 왼쪽이 통과)
if (age < 18 or age > 65) and not is_student or has_discount_code:
  print("할인 적용 대상입니다!")

print("-" * 30)


"""
Nested If Statements (중첩 If 문)
if 문 안에 또 다른 if 문을 넣을 수 있습니다. 이것을 "중첩 if 문"이라고 부릅니다.
점점 더 깊은 수준의 의사결정을 만들 수 있지만, 너무 많이 중첩되면 코드를 읽기 어려워집니다.
(때로는 `and` 연산자로 합치는 게 더 간결할 수도 있습니다)
"""

x = 41

if x > 10:
  print("10보다 크고,")
  # 첫 번째 조건이 참일 때만 안쪽으로 들어옵니다
  if x > 20: 
    print("그리고 20보다도 큽니다!")
  else:
    print("하지만 20보다 크지는 않습니다.")
    
print("-" * 30)


"""
The pass Statement (pass 문)
if 문의 내용에는 무조건 코드가 자리를 차지해야 합니다 (비워두면 에러가 납니다).
하지만 나중에 코드를 짜려고 임시 뼈대만 만들어 둘 때, 
`pass` 키워드를 넣어주면 아무 일도 안 하면서 문법 에러를 방지해주는 '자리 표시자(placeholder)' 역할을 합니다!
"""

score = 85

# 만약 90점을 넘는다면? -> 아직 안 정함! 나중에 짤 거임!
if score > 90:
  pass # 아무것도 안 하고 넘어갑니다 (하지만 코드는 정상 작동합니다)
else:
  print("점수 처리가 완료되었습니다.")

# 함수 뼈대만 만들 때도 잘 쓰입니다.
def calculate_discount(price):
  pass # TODO: 나중에 여기에 연산 로직을 넣을 예정
