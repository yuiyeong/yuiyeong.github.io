---
title: Python 실용 팁 01
date: 2025-04-01 17:15:00 +0900
categories: [PYTHON, ETC]
tags: ['급발진거북이', 'python']
toc: true
comments: false
mermaid: true
math: true
---

## 🔄 str과 repr의 차이점과 활용법

파이썬에서 객체를 문자열로 변환하는 방법은 여러 가지가 있는데, 그 중에서도 `str()`과 `repr()`은 서로 다른 목적을 가지고 있다.

### str() - 사용자를 위한 출력

`str()`은 객체의 '사용자 친화적인' 문자열 표현을 반환한다.


```python
# 정수
print(str(42))  # 출력: 42

# 리스트
print(str([1, 2, 3]))  # 출력: [1, 2, 3]

# 날짜
import datetime
today = datetime.datetime.now()
print(str(today))  # 출력: 2025-04-01 12:34:56.789012

```

### repr() - 개발자를 위한 출력

`repr()`은 객체의 '공식적인' 문자열 표현을 반환하며, 가능하면 객체를 재생성할 수 있는 Python 코드를 반환한다.


```python
# 정수
print(repr(42))  # 출력: 42

# 리스트
print(repr([1, 2, 3]))  # 출력: [1, 2, 3]

# 문자열
print(str('Hello'))     # 출력: Hello
print(repr('Hello'))    # 출력: 'Hello' (따옴표 포함)

# 날짜
import datetime
today = datetime.datetime.now()
print(repr(today))  # 출력: datetime.datetime(2025, 4, 1, 12, 34, 56, 789012)

```

### 주요 차이점

- **목적**:

	- `str()`: 사람이 읽기 쉬운 형태로 출력

	- `repr()`: 디버깅과 개발용으로, 객체를 재생성할 수 있는 정보 포함

- **특수문자 처리**:

	- `str()`: 특수문자를 그대로 보여줌

	- `repr()`: 이스케이프 시퀀스로 표시

	
```python
s = 'Hello\nWorld'
print(str(s))    # Hello
                 # World
print(repr(s))   # 'Hello\nWorld'

```

- **클래스 구현**:

	- `str()`: 객체의 `__str__` 메서드 호출

	- `repr()`: 객체의 `__repr__` 메서드 호출

### 사용자 정의 클래스에서의 활용


```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age}세"

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"

p = Person("홍길동", 30)
print(str(p))   # 출력: 홍길동, 30세
print(repr(p))  # 출력: Person(name='홍길동', age=30)

```

> 💡 직접 클래스를 만들 때는 최소한 `__repr__`은 구현하는 것이 좋다. 
`__str__`이 없으면 파이썬은 자동으로 `__repr__`을 사용하지만, 반대는 적용되지 않는다!

### 언제 무엇을 사용해야 할까?

- `**str()**`** 사용 시기**:

	- 최종 사용자에게 보여줄 텍스트

	- 로그 메시지

	- 사용자 인터페이스 표시

- `**repr()**`** 사용 시기**:

	- 디버깅

	- 개발 중 객체 검사

	- 로깅 시스템에서 객체의 정확한 상태 기록

	- Python 인터프리터에서 객체 검사 (기본적으로 REPL에서는 `repr` 사용)

## 🧩 eval() 함수 활용하기

`eval()`은 문자열로 표현된 Python 표현식을 평가하고 실행하는 함수다.


```python
x = 1
print(eval('x + 1'))  # 출력: 2

print(eval('[1, 2, 3] + [4, 5]'))  # 출력: [1, 2, 3, 4, 5]

# repr()로 만든 문자열은 보통 eval()로 다시 객체로 변환 가능
original_list = [1, 2, 3]
list_repr = repr(original_list)  # '[1, 2, 3]'
recreated_list = eval(list_repr)
print(recreated_list)  # 출력: [1, 2, 3]

```

### repr()과 eval()의 연결고리

`repr()`의 주요 목적 중 하나는 `eval(repr(obj)) == obj`가 가능하도록 하는 것이다. 이는 복잡한 객체를 문자열로 저장했다가 다시 복원할 때 유용하다.


```python
import datetime
today = datetime.datetime.now()
today_repr = repr(today)
print(today_repr)  # datetime.datetime(2025, 4, 1, 12, 34, 56, 789012)

# repr로 생성된 문자열을 eval로 다시 객체로 변환
recreated_date = eval(today_repr)
print(type(recreated_date))  # <class 'datetime.datetime'>
print(recreated_date == today)  # True

```

### eval() 사용 시기와 주의사항

**사용 시기**

- 동적으로 Python 코드 실행이 필요할 때

- 문자열로 저장된 데이터를 원래 형태로 복원할 때

- 간단한 수식 계산기 구현

> ⚠️ 사용자 입력을 직접 `eval()` 에 전달하면 심각한 보안 위험이 발생할 수 있다. 악의적인 코드 실행 가능성이 있기 때문에 주의해야 한다!


```python
# 위험한 예
user_input = "__import__('os').system('rm -rf /')" # 시스템 파일 삭제 명령
# eval(user_input)  # 절대 실행하지 말 것!

# 안전한 대안: ast.literal_eval 사용
import ast
safe_data = ast.literal_eval('[1, 2, 3]')  # 안전하게 리스트로 변환
print(safe_data)  # [1, 2, 3]

# 이런 코드는 ast.literal_eval에서는 오류 발생
# ast.literal_eval("__import__('os').system('ls')")  # 오류 발생, 실행 불가

```

`ast.literal_eval`은 리터럴(숫자, 문자열, 리스트, 딕셔너리 등)만 평가할 수 있어 더 안전하다.

## 🔍 파이썬의 클로저(Closure)와 데코레이터(Decorator)

파이썬 프로그래밍에서 클로저와 데코레이터는 강력한 기능을 제공하는 개념이다. 이 두 개념은 함수형 프로그래밍의 핵심적인 부분이며, 코드의 재사용성과 가독성을 높이는 데 큰 도움이 된다.

### 클로저(Closure)란?

클로저는 함수 안에 함수가 정의되어 있고, 내부 함수가 외부 함수의 변수를 참조할 때 생성되는 함수 객체이다.

### 클로저의 특징

- 함수 내부에 다른 함수가 정의됨

- 내부 함수가 외부 함수의 변수를 참조

- 외부 함수가 내부 함수를 반환

### 예시


```python
def outer_function(x):
    # 외부 함수의 변수
    outer_var = x

    # 내부 함수 정의
    def inner_function(y):
        # 외부 함수의 변수를 사용
        return outer_var + y

    # 내부 함수 반환
    return inner_function

# 클로저 생성
closure = outer_function(10)
# 클로저 실행
result = closure(5)  # 10 + 5 = 15
print(result)  # 출력: 15

```

위 코드에서 `inner_function`은 `outer_function`의 지역 변수인 `outer_var`를 참조하고 있다. `outer_function`이 실행을 완료한 후에도 반환된 `inner_function`은 여전히 `outer_var`의 값을 기억하고 있다. 이것이 바로 클로저의 핵심이다!

### 클로저의 응용 - 카운터


```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

counter = make_counter()
print(counter())  # 출력: 1
print(counter())  # 출력: 2
print(counter())  # 출력: 3

```

> 💡 여기서 `nonlocal` 키워드는 외부 함수의 변수를 내부 함수에서 수정할 수 있게 해준다. 이것이 없으면 내부 함수에서 외부 함수의 변수를 읽을 수만 있고 수정할 수 없다!

### 데코레이터(Decorator)란?

데코레이터는 함수를 인자로 받아 기능을 확장하고 다시 함수를 반환하는 함수이다. 파이썬에서는 `@` 기호를 사용해 데코레이터를 적용한다.

### 데코레이터의 특징

- 기존 함수를 수정하지 않고 기능을 확장

- 코드 재사용성 증가

- 함수의 전처리/후처리 가능

### 기본 데코레이터 예시


```python
def my_decorator(func):
    def wrapper():
        print("함수 실행 전")
        func()
        print("함수 실행 후")
    return wrapper

@my_decorator
def say_hello():
    print("안녕하세요!")

# 데코레이터 사용
say_hello()
# 출력:
# 함수 실행 전
# 안녕하세요!
# 함수 실행 후

```

`@my_decorator` 구문은 사실 다음과 동일하다.


```python
say_hello = my_decorator(say_hello)

```

이렇게 데코레이터는 함수를 다른 함수로 감싸서 기능을 확장하는 문법적 설탕(Syntactic Sugar)이다.

### 인자를 받는 함수에 데코레이터 적용


```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("함수 실행 전")
        result = func(*args, **kwargs)
        print("함수 실행 후")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

result = add(3, 5)
print(f"결과: {result}")
# 출력:
# 함수 실행 전
# 함수 실행 후
# 결과: 8

```

여기서 `*args`와 `**kwargs`를 사용하면 어떤 인자라도 전달할 수 있는 범용 데코레이터를 만들 수 있다.

### 인자를 받는 데코레이터


```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"안녕하세요, {name}님!")
    return "완료"

result = say_hello("홍길동")
# 출력:
# 안녕하세요, 홍길동님!
# 안녕하세요, 홍길동님!
# 안녕하세요, 홍길동님!

```

`@repeat(3)`은 `say_hello = repeat(3)(say_hello)`와 동일하다. 외부 함수 `repeat`이 인자 `n`을 받고, 내부 함수 `decorator`가 실제 데코레이터 역할을 한다.

### 클로저와 데코레이터의 관계

클로저와 데코레이터는 밀접한 관계가 있다.

- 데코레이터는 클로저를 활용한 구현: 대부분의 데코레이터는 클로저 패턴을 사용하여 구현된다. 데코레이터 내부의 wrapper 함수는 외부 함수의 변수(원본 함수)를 참조하는 클로저이다.

- 기능 확장의 차이

	- 클로저: 주로 상태 유지와 데이터 은닉에 초점

	- 데코레이터: 함수의 기능 확장과 횡단 관심사(cross-cutting concerns) 처리에 초점

- 구현 방식의 차이

	- 클로저: 내부 함수가 외부 함수의 변수를 저장하고 활용

	- 데코레이터: 함수를 인자로 받아 기능을 추가한 새로운 함수를 반환

### 클로저와 데코레이터를 함께 사용하는 예시


```python
def counter_decorator(func):
    call_count = 0  # 클로저 변수

    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"함수 '{func.__name__}'이(가) {call_count}번째 호출되었습니다.")
        return func(*args, **kwargs)

    return wrapper

@counter_decorator
def hello(name):
    return f"안녕하세요, {name}님!"

print(hello("철수"))  # 함수 'hello'이(가) 1번째 호출되었습니다. \n 안녕하세요, 철수님!
print(hello("영희"))  # 함수 'hello'이(가) 2번째 호출되었습니다. \n 안녕하세요, 영희님!

```

이 예시에서,

- `counter_decorator`는 데코레이터 함수이다.

- `wrapper` 함수는 외부 함수의 `call_count` 변수를 참조하는 클로저이다.

- 데코레이터는 `hello` 함수의 기능을 확장하여 호출 횟수를 세는 기능을 추가한다.

- 클로저는 호출 횟수(`call_count`)를 유지하는 상태 관리 기능을 제공한다.

## 🚀 실용적인 데코레이터 예시

### 실행 시간 측정 데코레이터


```python
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 함수 실행 시간: {end_time - start_time:.5f}초")
        return result
    return wrapper

@measure_time
def slow_function():
    time.sleep(1)
    return "작업 완료"

slow_function()  # slow_function 함수 실행 시간: 1.00123초

```

### 캐싱(메모이제이션) 데코레이터


```python
def memoize(func):
    cache = {}  # 클로저 변수로 캐시 저장

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(35))  # 매우 빠르게 계산됨

```

## 🧮 collections.Counter로 요소 세기

파이썬의 `collections` 모듈에는 데이터 처리에 유용한 여러 컨테이너 타입이 있는데, 그 중에서도 `Counter`는 요소의 개수를 세는 작업을 매우 쉽게 만들어준다.

### Counter 기본 사용법

`Counter`는 해시 가능한 객체를 세는 dict의 서브클래스다. 요소를 키로, 개수를 값으로 저장한다.


```python
from collections import Counter

# 문자열에서 각 문자의 등장 횟수 세기
c = Counter('hello world')
print(c)  # Counter({'l': 3, 'o': 2, ' ': 1, 'h': 1, 'e': 1, 'w': 1, 'r': 1, 'd': 1})

# 리스트에서 요소 개수 세기
fruits = ['apple', 'orange', 'apple', 'banana', 'orange', 'apple']
fruit_counter = Counter(fruits)
print(fruit_counter)  # Counter({'apple': 3, 'orange': 2, 'banana': 1})

```

### Counter의 유용한 메서드

### most_common() - 가장 흔한 요소 찾기


```python
# 가장 흔한 요소부터 내림차순으로 모든 요소 반환
print(fruit_counter.most_common())  # [('apple', 3), ('orange', 2), ('banana', 1)]

# 상위 n개 요소만 반환
print(fruit_counter.most_common(2))  # [('apple', 3), ('orange', 2)]

```

### elements() - 요소 반복하기

각 요소를 그 개수만큼 반복해서 반환한다:


```python
c = Counter(a=3, b=1, c=0)
print(list(c.elements()))  # ['a', 'a', 'a', 'b']
# 참고: 개수가 0 이하인 요소는 elements()에서 무시됨

```

### update() - 카운터 갱신하기

다른 카운터나 반복 가능한 객체로 카운터를 갱신한다:


```python
c = Counter(['apple', 'orange'])
c.update(['apple', 'banana', 'banana'])
print(c)  # Counter({'apple': 2, 'banana': 2, 'orange': 1})

```

### subtract() - 카운터 뺄셈

다른 카운터의 개수를 뺀다:


```python
c = Counter(a=4, b=2, c=0)
d = Counter(a=1, b=2, c=3)
c.subtract(d)
print(c)  # Counter({'a': 3, 'b': 0, 'c': -3})

```

### Counter의 수학 연산

`Counter` 객체는 다양한 수학 연산을 지원한다:


```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

# 합집합 (최댓값 취함)
print(c1 | c2)  # Counter({'a': 3, 'b': 2})

# 교집합 (최솟값 취함)
print(c1 & c2)  # Counter({'a': 1, 'b': 1})

# 덧셈
print(c1 + c2)  # Counter({'a': 4, 'b': 3})

# 뺄셈 (음수 결과는 삭제됨)
print(c1 - c2)  # Counter({'a': 2})

```

### 실용적인 활용 예시

### 텍스트 분석: 단어 빈도 계산


```python
import re
from collections import Counter

def word_frequency(text):
    # 소문자로 변환하고 단어만 추출
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

sample_text = """
Python is a programming language that lets you work quickly
and integrate systems more effectively. Python is powerful... and fast;
plays well with others; runs everywhere; is friendly & easy to learn;
is Open Source; has a vibrant community.
"""

word_counts = word_frequency(sample_text)
print(word_counts.most_common(5))
# [('is', 3), ('python', 2), ('and', 2), ('to', 1), ('a', 1)]

```

### 데이터 검증: 중복 항목 찾기


```python
from collections import Counter

def find_duplicates(items):
    counts = Counter(items)
    return {item: count for item, count in counts.items() if count > 1}

user_ids = [101, 102, 103, 101, 104, 105, 102, 106]
print(find_duplicates(user_ids))  # {101: 2, 102: 2}

```

### 투표 집계


```python
from collections import Counter

votes = ['John', 'Jane', 'John', 'Jack', 'Jane', 'John', 'Jane', 'Jack', 'John', 'Mary']

vote_counts = Counter(votes)
winner = vote_counts.most_common(1)[0][0]

print(f"투표 결과: {dict(vote_counts)}")  # 투표 결과: {'John': 4, 'Jane': 3, 'Jack': 2, 'Mary': 1}
print(f"당선자: {winner} ({vote_counts[winner]}표)")  # 당선자: John (4표)

```

> 💡 Counter는 딕셔너리의 서브클래스이므로 dict의 모든 기능을 사용할 수 있다. Counter 객체는 in 연산이나 get() 메서드 등 딕셔너리의 모든 메서드를 지원한다!

### Counter와 defaultdict의 차이

`collections` 모듈에는 `defaultdict`라는 비슷한 컨테이너도 있다. 둘의 주요 차이점은,

- `Counter`는 키가 없으면 0을 반환하고, `defaultdict`는 지정한 기본값을 반환한다.

- `Counter`는 요소 개수 세기에 최적화되어 있고 `most_common()` 같은 특수 메서드를 제공한다.

- `defaultdict`는 더 일반적인 목적으로 사용되며 원하는 타입의 기본값을 설정할 수 있다.


```python
from collections import Counter, defaultdict

c = Counter()
d = defaultdict(int)

# 존재하지 않는 키에 접근
print(c['non-existent'])  # 0 (Counter는 기본값이 0)
print(d['non-existent'])  # 0 (defaultdict(int)의 기본값도 0)

# 하지만 defaultdict는 다른 타입의 기본값도 가능
string_dict = defaultdict(str)
list_dict = defaultdict(list)

print(string_dict['non-existent'])  # '' (빈 문자열)
print(list_dict['non-existent'])    # [] (빈 리스트)

```

<br/>

