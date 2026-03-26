# 09_Strings
print('Hello from 09_Strings')


print("Hello")
print('Hello') # 위 두개 같은거임)

print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')
# 문자열은 큰따옴표 또는 작은따옴표로 묶을 수 있습니다.
# 문자열 안에 작은따옴표가 포함되어 있으면 큰따옴표로 묶어야 하고,
#  문자열 안에 큰따옴표가 포함되어 있으면 작은따옴표로 묶어야 합니다.


#변수에 문자열을 할당하려면 변수 이름 뒤에 등호(=)와 문자열을 입력합니다.

a = "Hello"
print(a)


#세 개의 따옴표를 사용하면 여러 줄로 된 문자열을 변수에 할당할 수 있습니다.

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)


a = "Hello, World!"
print(a[1]) #( 문자열에 0번째에 H가 저장됨)


# 바나나 문자를 하나씩 출력하기
for x in "banana":
  print(x)


#문자열 길이 구하기
a = "Hello, World!"
print(len(a))

#문자열에 특정 구문이나 문자가 있는지 확인하려면 키워드를 사용할 수 있습니다 in.

txt = "The best things in life are free!"
print("free" in txt)

# 문자에 "free" 가 포함되면  출력
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

#2번째 위치부터 5번째 위치까지의 문자를 가져옵니다(포함되지 않음):

#2번쨰 위치부터 5번째 위치 문자 출력
b = "Hello, World!"
print(b[2:5])

# 시작부터 5번째 문자 출력
b = "Hello, World!"
print(b[:5])

#2번째 위치부터 끝까지 문자 출력
b = "Hello, World!"
print(b[2:])


b = "Hello, World!"
print(b[-5: -3]) # -5번째 위치부터 -3번째 위치까지의 문자 출력

#이 upper()메서드는 문자열을 대문자로 반환합니다.


a = "Hello, World!"
print(a.upper())

#이 lower()메서드는 문자열을 소문자로 반환합니다

a = "Hello, World!"
print(a.lower())

#공백은 실제 텍스트 앞뒤에 있는 공간이며, 이 공백을 제거해야 하는 경우가 매우 많습니다.

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"


#이 replace()메서드는 문자열을 다른 문자열로 바꿉니다.

a = "Hello, World!"
print(a.replace("H", "J")) # returns "Jello, World!"

a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']


#a변수와 변수를 병합하여 b하나의 변수로 만듭니다 c.

a = "Hello"
b = "World"
c = a + b
print(c)


#두 글자 사이에 공백을 넣으려면 콜론(:)을 추가하세요 " ".

a = "Hello"
b = "World"
c = a + " " + b
print(c)




#F-스트링
#F-String은 Python 3.6에서 도입되었으며, 현재 문자열 형식을 지정하는 데 권장되는 방법입니다.

#문자열을 f-문자열로 지정하려면 문자열 리터럴 앞에 f를 붙이고 
# {}변수 및 기타 연산을 위한 자리 표시자로 중괄호를 추가하면 됩니다.
age = 36
txt = f"My name is John, I am {age}"
print(txt)



price = 59
txt = f"The price is {price} dollars"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars" #.2f는 price변수를 소수점 2자리까지 표시하도록 지정합니다.
print(txt)


txt = f"The price is {20 * 59} dollars" # 플레이스 홀더 안에 파이썬 코드 포함 가능
print(txt)

# 따움표 안에 따움표 넣는법
txt = "We are the so-called \"Vikings\" from the north."


# \'	Single Quote	
# \\	Backslash	
# \n	New Line	
# \r	Carriage Return	
# \t	Tab	
# \b	Backspace	
# \f	Form Feed	
# \ooo	Octal value	
# \xhh	Hex value

# --- 문자열 메서드 ---
# capitalize()	첫 글자를 대문자로 변환합니다
# casefold()	문자열을 소문자로 변환합니다 (보다 강력한 lower())
# center()	문자열을 중앙 정렬하여 반환합니다
# count()	문자열에서 지정된 값이 나타나는 횟수를 반환합니다
# encode()	문자열의 인코딩된 버전을 반환합니다
# endswith()	문자열이 지정된 값으로 끝나면 True를 반환합니다
# expandtabs()	문자열의 탭 크기를 설정합니다
# find()	문자열에서 지정된 값을 검색하고 찾은 위치를 반환합니다
# format()	문자열 내의 지정된 값을 형식화합니다
# format_map()	문자열 내의 지정된 값을 형식화합니다 (매핑 객체 사용)
# index()	문자열에서 지정된 값을 검색하고 찾은 위치를 반환합니다
# isalnum()	문자열의 모든 문자가 알파벳이나 숫자인 경우 True를 반환합니다
# isalpha()	문자열의 모든 문자가 알파벳인 경우 True를 반환합니다
# isascii()	문자열의 모든 문자가 ASCII 문자인 경우 True를 반환합니다
# isdecimal()	문자열의 모든 문자가 십진수인 경우 True를 반환합니다
# isdigit()	문자열의 모든 문자가 숫자인 경우 True를 반환합니다
# isidentifier()	문자열이 유효한 식별자인 경우 True를 반환합니다
# islower()	문자열의 모든 문자가 소문자인 경우 True를 반환합니다
# isnumeric()	문자열의 모든 문자가 숫자인 경우 True를 반환합니다
# isprintable()	문자열의 모든 문자가 인쇄 가능한 문자인 경우 True를 반환합니다
# isspace()	문자열의 모든 문자가 공백인 경우 True를 반환합니다
# istitle()	문자열이 제목 형식 규칙을 따르는 경우 True를 반환합니다
# isupper()	문자열의 모든 문자가 대문자인 경우 True를 반환합니다
# join()	반복 가능한 객체의 요소를 문자열의 끝에 연결합니다
# ljust()	문자열을 왼쪽 정렬하여 반환합니다
# lower()	문자열을 소문자로 변환합니다
# lstrip()	문자열의 왼쪽 공백 트리밍 버전을 반환합니다
# maketrans()	변환에 사용할 변환 테이블을 반환합니다
# partition()	문자열을 세 부분으로 나눈 튜플을 반환합니다
# replace()	지정된 값이 지정된 다른 값으로 교체된 문자열을 반환합니다
# rfind()	문자열에서 지정된 값을 검색하고 찾은 마지막 위치를 반환합니다
# rindex()	문자열에서 지정된 값을 검색하고 찾은 마지막 위치를 반환합니다
# rjust()	문자열을 오른쪽 정렬하여 반환합니다
# rpartition()	문자열을 세 부분으로 나눈 튜플을 반환합니다
# rsplit()	지정된 구분자를 기준으로 문자열을 분할하고 리스트를 반환합니다
# rstrip()	문자열의 오른쪽 공백 트리밍 버전을 반환합니다
# split()	지정된 구분자를 기준으로 문자열을 분할하고 리스트를 반환합니다
# splitlines()	줄 바꿈을 기준으로 문자열을 분할하고 리스트를 반환합니다
# startswith()	문자열이 지정된 값으로 시작하면 True를 반환합니다
# strip()	문자열의 양쪽 공백 트리밍 버전을 반환합니다
# swapcase()	대소문자를 바꿉니다. 소문자는 대문자로, 대문자는 소문자로 변환됩니다
# title()	각 단어의 첫 글자를 대문자로 변환합니다
# translate()	변환된 문자열을 반환합니다
# upper()	문자열을 대문자로 변환합니다
# zfill()	지정된 수만큼 문자열의 시작 부분에 0 값을 채웁니다



# Create the variable 
txt = "Hello, World!"
# Print characters from index 2 to 5
print(txt[2:5])
# Print in upper case
print( txt.upper())
# Create the name variable
name = "Python"
# Print using an f-string # 막혔던거
print(f"I love {name}")