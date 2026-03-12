# 06_Data_Types
print('Hello from 06_Data_Types')

#프로그래밍에서 데이터 타입은 중요한 개념입니다.

# 변수는 다양한 유형의 데이터를 저장할 수 있으며, 유형별로 수행할 수 있는 작업이 다릅니다.

# 파이썬은 기본적으로 다음과 같은 데이터 유형을 내장하고 있습니다(범주별):


""" # 텍스트 유형:	str
# 숫자 유형:	int, float, complex
# 시퀀스 유형:	list, tuple, range
# 매핑 유형:	dict
# 세트 유형:	set,frozenset
# 부울 유형:	bool
# 이진 유형:	bytes, bytearray, memoryview
# 없음 유형:	NoneType """


x = "Hello World"	#str
x = 20	#int	
x = 20.5	#float	
x = 1j	#complex	
x = ["apple", "banana", "cherry"]	#list	
x = ("apple", "banana", "cherry")	#tuple	
x = range(6)	#range	
x = {"name" : "John", "age" : 36}	#dict	
x = {"apple", "banana", "cherry"}	#set	
x = frozenset({"apple", "banana", "cherry"})	#frozenset	
x = True	#bool	
x = b"Hello"	#bytes	
x = bytearray(5)	#bytearray	
x = memoryview(bytes(5))	#memoryview	
x = None	#NoneType



#_____________________________________________________________________
# 변수 할당

x = str("Hello World")	#str	
x = int(20)	#int	
x = float(20.5)	#float	
x = complex(1j)	#complex	
x = list(("apple", "banana", "cherry"))	#list	
x = tuple(("apple", "banana", "cherry"))	#tuple	
x = range(6)	#range	
x = dict(name="John", age=36)	#dict	
x = set(("apple", "banana", "cherry"))	#set	
x = frozenset(("apple", "banana", "cherry"))	#frozenset	
x = bool(5)	#bool	
x = bytes(5)	#bytes	
x = bytearray(5)	#bytearray	
x = memoryview(bytes(5))	#memoryview