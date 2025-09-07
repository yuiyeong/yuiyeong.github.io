---
title: 🐍 고급 자료 구조(w. Python)
date: 2025-04-16 18:28:00 +0900
categories: [ PYTHON, CODING_TEST ]
tags: [ '급발진거북이', 'python', '자료구조', 'data structure', '파이썬', '코딩테스트', 'GeekAndChill', '기깬칠' ]
toc: true
comments: false
mermaid: true
math: true
---

## 📦 사용하는 python package

- Python 3.11+

- collections 모듈 (Counter, defaultdict)

- heapq 모듈

- NumPy (1.20+)

- Pandas (1.3+)

## 🚀 TL;DR

- Counter 는 요소의 빈도수를 쉽게 계산할 수 있는 딕셔너리 확장 클래스로, 데이터 분석에 유용함

- defaultdict 는 키가 없을 때 자동으로 기본값을 생성하여 코드를 간결하게 만들어 줌

- 우선 순위 큐는 요소가 우선순위에 따라 처리되는 자료구조로, 힙을 통해 효율적으로 구현됨

- 힙은 O(log n)의 삽입/삭제로 최소값 또는 최대값에 빠르게 접근할 수 있는 완전 이진 트리

- NumPy 와 Pandas 는 데이터 과학에 최적화된 자료구조로, 기존 파이썬 리스트 / 딕셔너리보다 대용량 데이터 처리에 효율적임

## 📦✨ collections 모듈 소개

파이썬의 `collections` 모듈은 기본 내장 컨테이너(`list`, `tuple`, `dict`, `set`) 외에, 특정한 목적에 더 효율적이거나 편리한 추가적인 컨테이너 데이터 타입들을 제공하는 모듈이다.

### **주요 제공 클래스**

- `deque`: 양쪽 끝에서 빠른 추가/삭제가 가능한 리스트 유사 컨테이너 (스택, 큐 구현에 효율적)

- `namedtuple()`: 필드 이름을 가진 튜플 서브클래스 팩토리 함수 (튜플처럼 불변이지만, 인덱스 대신 이름으로 필드 접근 가능)

- `Counter`: 해시 가능한 객체를 세는 데 특화된 딕셔너리 서브클래스

- `defaultdict`: 키가 없을 때 기본값을 자동으로 생성해주는 딕셔너리 서브클래스

- `OrderedDict`: (Python 3.7 이전 버전에서) 삽입 순서를 기억하는 딕셔너리 (3.7+ 부터는 일반 `dict`도 순서 유지)

- `ChainMap`: 여러 매핑(딕셔너리 등)을 하나의 뷰로 연결

- `UserDict`, `UserList`, `UserString`: 사용자 정의 클래스를 만들 때 상속하기 위한 래퍼 클래스

## 📊🔢 collections.Counter - 빈도수 계산 전문가

- 시퀀스나 다른 반복 가능한(iterable) 객체 내의 **해시 가능한(hashable) 객체들의 개수(빈도수)** 를 세는 데 특화된 **딕셔너리 서브클래스**

- 어떤 요소가 몇 번 나타났는지 {요소: 개수} 형태의 딕셔너리로 저장

- *존재하지 않는 요소에 접근하면 KeyError 대신 0 을 반환. (일반 딕셔너리와 다른 점!)*

- 내부적으로 dict(해시 테이블)를 사용하여 각 요소의 개수를 저장

- 활용 예시)

    - 텍스트 분석에서 단어/문자 빈도수 계산

    - 로그 분석에서 이벤트 발생 횟수 집계

    - 투표 결과 등 항목별 개수 집계

    - 두 데이터 그룹 간의 공통/차이 요소 개수 비교 (멀티셋 연산)

    - 아나그램(Anagram) 검사

```python
from collections import Counter

# 문자열에서 생성 (각 문자의 빈도수 계산)
c = Counter('hello world')  # Counter({'l': 3, 'o': 2, ' ': 1, 'h': 1, 'e': 1, 'w': 1, 'r': 1, 'd': 1})

# 리스트에서 생성 (각 요소의 빈도수 계산)
c = Counter(['apple', 'orange', 'apple', 'banana', 'apple'])  # Counter({'apple': 3, 'orange': 1, 'banana': 1})

# 딕셔너리에서 생성 (이미 카운트된 값으로 초기화)
c = Counter({'apple': 3, 'orange': 1, 'banana': 1})  # 위와 동일

# 키워드 인자로 생성
c = Counter(apple=3, orange=1, banana=1)  # 위와 동일
```

### 주요 메서드 및 특징

- 딕셔너리 메서드 대부분 사용 가능: `keys()`, `values()`, `items()`, `get()`, `pop()`, `len()` 등

- `most_common(n)`: 빈도수가 가장 높은 `n`개의 요소와 그 개수를 (요소, 개수) 튜플의 리스트로 반환

    - `n` 생략 시 모든 요소를 빈도수 내림차순으로 반환

- `elements()`: 각 요소를 자신의 개수만큼 반복하는 이터레이터(iterator) 반환(순서는 임의적일 수 있음)

- `update(iterable or mapping)`: 다른 `Counter`나 iterable/mapping으로 현재 `Counter`의 개수를 갱신(더함)

- `subtract(iterable or mapping)`: 다른 `Counter`나 iterable/mapping으로 현재 `Counter`의 개수를 뺌 (결과가 음수나 0이 될 수 있음)

- 산술 연산자: `+`, , `&`(교집합: min), `|`(합집합: max) 연산 가능

    - 결과는 0 이하 개수 제외

- *존재하지 않는 키 접근: *`*my_counter['unknown_key']*`* → 0 반환 (KeyError 없음!)*

- 대부분의 연산이 내부 딕셔너리 연산에 의존하므로 평균 O(1) 또는 O(k) (k는 관련 요소 수)

- `most_common`은 정렬이 필요하므로 O(N log N) 또는 O(N log k) (N은 고유 요소 수, k는 n)

```python
from collections import Counter

# 텍스트의 단어 빈도수 계산
text = "to be or not to be that is the question"
word_counts = Counter(text.split())
print(word_counts)  # Counter({'to': 2, 'be': 2, 'or': 1, 'not': 1, 'that': 1, 'is': 1, 'the': 1, 'question': 1})

# 가장 많이 등장하는 단어 2개 찾기
most_common = word_counts.most_common(2)
print(most_common)  # [('to', 2), ('be', 2)]

# 모든 요소를 개수만큼 열거
print(list(word_counts.elements()))  # ['to', 'to', 'be', 'be', 'or', 'not', 'that', 'is', 'the', 'question']

# Counter 객체 업데이트
more_text = "to be a programmer or not to be a programmer"
word_counts.update(more_text.split())
print(word_counts)  # Counter가 업데이트됨

# 멀티셋 연산
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})  # 음수나 0인 개수는 제외됨

```

## 🏭🔑👍 collections.defaultdict - 똑똑한 비서 딕셔너리

일반 딕셔너리(`dict`)의 서브클래스로, 존재하지 않는 키(Key) 에 접근하려고 할 때 KeyError 를 발생시키는 대신, 미리 지정된 기본값 생성 함수(`default_factory`) 를 호출하여 그
결과를 새로운 값으로 설정하고 반환해주는 딕셔너리

⇒ "이 키 없으면, 이걸로 기본값 만들어서 넣어줘!"

### `default_factory`

- `defaultdict`를 생성할 때 **첫 번째 인자**로 전달되는 함수 또는 호출 가능한 객체

- 인자를 받지 않고 호출 가능해야 함 (`callable()`)

- 예시) `list`, `int`, `set`, `float`, `str`, `lambda: "default"` 등

- 만약 `default_factory`가 `None`으로 설정되면 (또는 지정되지 않으면), 일반 dict 처럼 없는 키 접근 시 `KeyError` 발생

### 동작 방식

- `my_defaultdict[key]` 로 키에 접근 시도(dict 와 같은 시간 복잡도)

- `key`가 딕셔너리에 이미 존재하면 → 해당 값을 반환 (일반 dict 와 동일)

- `key`가 딕셔너리에 존재하지 않으면, (평균 O(1))
  a. `default_factory`를 호출하여 기본값을 생성 (`value = default_factory()`)
  b. 생성된 기본값을 `key`의 값으로 딕셔너리에 삽입 (`my_defaultdict[key] = value`)
  c. 생성된 기본값 `value`를 반환

### 장점

- 키 존재 여부를 미리 확인할 필요 없이 바로 값에 접근하거나 수정 가능 → 코드가 매우 간결해짐!

- 특히 리스트나 집합 등에 아이템을 그룹화하거나, 카운트를 누적하는 로직을 쉽게 구현 가능

```python
from collections import defaultdict

# 일반 딕셔너리 사용 시
d = {}
for key in ['a', 'b', 'c', 'a', 'b', 'a']:
    if key not in d:  # 키 존재 여부 확인 필요!
        d[key] = 0
    d[key] += 1

# defaultdict(int) 사용 시
d = defaultdict(int)
for key in ['a', 'b', 'c', 'a', 'b', 'a']:
    d[key] += 1  # 키가 없어도 자동으로 int()=0 생성 후 +1

# list 기본값
dd_list = defaultdict(list)
for key, value in [('a', 1), ('b', 2), ('a', 3), ('b', 4), ('c', 5)]:
    dd_list[key].append(value)  # 키가 없으면 빈 리스트 생성 후 추가
print(dd_list)  # defaultdict(<class 'list'>, {'a': [1, 3], 'b': [2, 4], 'c': [5]})

# int 기본값
dd_int = defaultdict(int)
for word in "hello world hello".split():
    dd_int[word] += 1  # 단어 빈도수 계산, 키가 없으면 0 생성 후 +1
print(dd_int)  # defaultdict(<class 'int'>, {'hello': 2, 'world': 1})

# set 기본값
dd_set = defaultdict(set)
for key, value in [('a', 1), ('b', 2), ('a', 3), ('b', 2)]:
    dd_set[key].add(value)  # 키가 없으면 빈 집합 생성 후 추가 (중복 제거됨)
print(dd_set)  # defaultdict(<class 'set'>, {'a': {1, 3}, 'b': {2}})

# 람다 기본값
dd_lambda = defaultdict(lambda: "Not Available")
dd_lambda['known'] = "Value exists"
print(dd_lambda['known'])  # 'Value exists'
print(dd_lambda['unknown'])  # 'Not Available' (키가 없으면 기본값 생성)
```

> ❗주의: `defaultdict`는 없는 키에 접근할 때 자동으로 해당 키-값 쌍을 생성하므로, 단순히 키 존재 여부만 확인하고 싶을 때는 일반 `in` 연산자를 사용하는 것이 좋습니다. (
`key in my_defaultdict`)
`my_defaultdict[key]`를 사용해서 확인하게 되면, 의도치 않게 dict 를 변경할 수 있습니다.

## 🆚 Counter vs defaultdict(int) 비교

둘 다 요소의 개수를 세는 데 사용할 수 있지만, 약간의 차이가 있다.

| 특징          | `Counter`                              | `defaultdict(int)`           | 
 |-------------|----------------------------------------|------------------------------| 
| **주 목적**    | 빈도수 계산 및 관련 연산 (multiset)              | 키 부재 시 기본값(0) 제공, 일반 딕셔너리 확장 | 
| **상속 관계**   | `dict`의 서브클래스                          | `dict`의 서브클래스                | 
| **없는 키 접근** | `0` 반환                                 | `0` 반환 (및 해당 키 생성)           | 
| **초기화**     | Iterable, Mapping, Keyword Args 등 다양   | `default_factory=int` 지정 필요  | 
| **특수 메서드**  | `most_common()`, `elements()`, 산술 연산 등 | 없음 (dict 메서드 + 기본값 기능)       | 
| **음수/0 값**  | `subtract` 등으로 음수/0 값 가능               | 일반적으로 양수 카운트만 저장 (0은 가능)     | 
| **일반적 사용**  | 최종 빈도수 집계, 상위 N개 찾기 등에 유리              | 카운트 누적 과정 자체를 간결하게 할 때 유리    | 

> 💡 단순히 개수를 세는 과정만 간결하게 하려면 `defaultdict(int)`도 좋지만, 빈도수와 관련된 다양한 기능(`most_common` 등)을 활용하거나 최종 결과를 다룰 때는 `Counter`가 더
> 편리하고 강력하다.

## 🥇🥈🥉 우선순위 큐 (Priority Queue, PQ) 란?

일반적인 큐(FIFO)와 달리, 들어간 순서가 아니라 **정해진 우선순위(priority)** 에 따라 요소가 **추출(dequeue)** 되는 추상 자료형(ADT)

- 각 요소는 우선순위 값을 가짐

- 가장 높은 (또는 가장 낮은) 우선순위를 가진 요소가 항상 먼저 제거됨

### 주요 연산

- **Insert / Add**: 우선순위 큐에 요소를 추가

- **Extract-Max / Delete-Max**: 가장 높은 우선순위를 가진 요소를 제거하고 반환

- **Extract-Min / Delete-Min**: 가장 낮은 우선순위를 가진 요소를 제거하고 반환

- **Peek / Get-Max/Min**: 가장 높은/낮은 우선순위를 가진 요소를 확인만 하고 제거하지 않음

### **다양한 구현 방법**

- **정렬되지 않은 리스트를 이용했을 때**: 삽입 O(1), 삭제/확인 O(n) (매번 전체 탐색 필요)

- **정렬된 리스트를 이용했을 때**: 삽입 O(n) (정렬 위치 찾아 삽입), 삭제/확인 O(1) (맨 앞/뒤)

- **균형 이진 탐색 트리를 이용했을 때**: 삽입/삭제/확인 O(log n) (구현 복잡)

- **힙(Heap)을 이용했을 때**: 삽입/삭제 O(log n), 확인 O(1) (가장 일반적이고 효율적인 구현!)

### **왜 필요할까?**

단순히 들어온 순서가 아니라, **중요도나 특정 기준**에 따라 데이터를 처리해야 하는 많은 실제 문제 상황에서 이러한 자료구조가 필요하다.

## 🌲 힙(Heap) 자료구조

![comparing_trees.png](/assets/img/comparing_trees.png)

**완전 이진 트리(Complete Binary Tree)** 형태를 가지면서, **힙 속성(Heap Property)** 을 만족하는 특수한 트리 기반 자료구조(우선순위 큐 구현에 가장 널리 사용)

### 완전 이진 트리 (Complete Binary Tree)

- 마지막 레벨을 제외한 모든 레벨이 완전히 채워져 있음

- 마지막 레벨의 노드들은 왼쪽부터 차례대로 채워져 있음

- 이 구조 덕분에 힙을 배열(리스트) 을 사용하여 효율적으로 표현 가능!

    - 노드 `i`의 왼쪽 자식: `2*i + 1`

    - 노드 `i`의 오른쪽 자식: `2*i + 2`

    - 노드 `i`의 부모: `(i - 1) // 2` (정수 나눗셈)

### 힙 속성 (Heap Property)

- 부모 노드와 자식 노드 간의 값(우선순위) 관계에 대한 규칙

- **최소 힙 (Min Heap)**: 모든 부모 노드의 값은 각 자식 노드의 값보다 작거나 같다 (<=)

    - 즉, **루트(root) 노드가 가장 작은 값**을 가짐.

- **최대 힙 (Max Heap)**: 모든 부모 노드의 값은 각 자식 노드의 값보다 크거나 같다 (>=)

    - 즉, **루트(root) 노드가 가장 큰 값**을 가짐.

### 주요 연산 및 시간 복잡도

- **삽입 (Insert)**

    - 새 요소를 트리의 마지막 위치(배열 끝)에 추가

    - 힙 속성을 만족할 때까지 부모 노드와 비교/교환하며 위로 이동 (Up-heap / Percolate-up)

    - *O(log n)* (트리의 높이만큼 비교/교환)

- **최소/최대값 삭제 (Extract-Min/Max)**

    - 루트 노드(최소/최대값)를 제거하고 저장

    - 트리의 마지막 노드를 루트 자리로 이동

    - 힙 속성을 만족할 때까지 자식 노드와 비교/교환하며 아래로 이동 (Down-heap / Percolate-down / Heapify-down) (최소 힙은 더 작은 자식과, 최대 힙은 더 큰 자식과 교환)

    - *O(log n)* (트리의 높이만큼 비교/교환)

- **최소/최대값 확인 (Peek)**: 루트 노드(배열의 첫 번째 요소)를 확인

    - *O(1)*

- **힙 생성 (Heapify)**: 정렬되지 않은 배열을 힙 구조로 변환

    - *O(n)*

    - 모든 노드에 대해 down-heap 수행, 리프 노드는 제외 가능하여 효율적

### 왜 우선순위 큐 구현에 효율적인가?

가장 중요한 연산인 *삽입과 우선순위 높은 요소 삭제가 모두 O(log n)* 으로 매우 빠르기 때문에!

## 🐍🔽 파이썬 heapq 모듈 - 리스트를 힙으로!

파이썬 표준 라이브러리로, **일반적인 리스트(list)** 를 **최소 힙(Min Heap)** 처럼 다룰 수 있게 해주는 함수들을 제공

- 별도의 힙 클래스를 제공하는 것이 아니라, **기존 리스트를 직접 수정(in-place)** 하여 힙 속성을 유지

- 기본적으로 **최소 힙**만 지원(최대 힙은 약간의 트릭 필요)

### 주요 함수

- `heapq.heappush(heap, item)`

    - `heap`(리스트)에 `item`을 **힙 속성을 유지하면서 추가**(O(log n))

    - 리스트의 `append` 후 up-heap 하는 것과 유사

- `heapq.heappop(heap)`:

    - `heap`(리스트)에서 **가장 작은 요소(루트) 를 제거하고 반환 → 힙 속성 유지**(O(log n))

    - 리스트가 비어있으면 `IndexError` 발생

    - 루트 제거 후 마지막 요소 루트로 옮기고 down-heap 하는 것과 유사

- `heapq.heapify(x)`

    - 리스트 `x`를 **제자리에서(in-place) 최소 힙 구조로 변환**(O(n))

    - *이미 리스트가 있을 때 한 번에 힙으로 만들고 싶을 때 사용*

- `heapq.heappushpop(heap, item)`:

    - `heap`에 `item`을 **push 한 다음, 가장 작은 요소를 pop**

    - *push 와 pop 을 따로 하는 것보다 효율적(O(log n))*

    - 힙의 크기를 일정하게 유지하면서 새 요소를 넣고 가장 작은 것을 버릴 때 유용

- `heapq.heapreplace(heap, item)`

    - `heap`에서 **가장 작은 요소를 pop 한 다음, 새로운 `item`을 push**

    - `heappushpop`과 순서 반대 (O(log n))

    - 힙이 비어있으면 `IndexError`

    - 힙의 크기가 변하지 않음

- `heapq.nsmallest(n, iterable, key=None)`:

    - `iterable`에서 **가장 작은 n 개의 요소를 리스트로 반환**

    - 힙 기반으로 효율적

- `heapq.nlargest(n, iterable, key=None)`:

    - `iterable`에서 **가장 큰 n 개의 요소를 리스트로 반환**

    - 힙 기반으로 효율적

```python
import heapq

# 빈 리스트로 시작
heap = []

# 요소 추가
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heap)  # [1, 5, 3] - 최소 힙 속성 유지 (루트=1)

# 가장 작은 요소 제거 및 반환
smallest = heapq.heappop(heap)
print(smallest)  # 1
print(heap)  # [3, 5] - 힙 속성 유지

# 기존 리스트를 힙으로 변환
numbers = [5, 8, 2, 1, 7, 3]
heapq.heapify(numbers)
print(numbers)  # [1, 5, 2, 8, 7, 3] - 최소 힙으로 재배치

# 가장 작은 요소 확인 (제거하지 않음)
print(numbers[0])  # 1

# 가장 작은 n개 요소 찾기
smallest_3 = heapq.nsmallest(3, numbers)
print(smallest_3)  # [1, 2, 3]
```

## 🥇🥈🌲 heapq로 우선순위 큐 구현하기

### 최소 우선순위 큐 (Min PQ)

- `heapq`는 기본적으로 최소 힙이므로, 그냥 사용하면 된다.

- `heappush`로 요소 추가, `heappop`으로 가장 작은(우선순위 높은) 요소 추출

### 최대 우선순위 큐 (Max PQ)

- `heapq`는 최소 힙만 지원하므로, *트릭 필요*

- **방법 1: 값의 부호 변경**

    - 저장할 때 값의 부호를 **음수(-)로 바꿔서** `heappush`

    - `heappop`으로 꺼낸 후 다시 부호를 바꿔서 원래 값으로 사용

    - *최소 힙에서, 가장 작은 값 = 원래 값 중 가장 큰 값*

- **방법 2: 튜플 사용**

    - `(우선순위, 데이터)` 형태의 tuple 을 저장

    - 파이썬 tuple 은 첫 번째 요소부터 순서대로 비교하므로, `heapq`는 우선순위를 기준으로 최소 힙을 만듦.

    - 최대 힙을 원하면 `(-우선순위, 데이터)` 형태로 저장

### 복잡한 객체 저장 및 안정성 (Tie-Breaking)

- tuple `(priority, item)` 사용 시, `priority`가 같으면 그 다음 요소인 `item`을 비교하게 됨. `item`이 비교 불가능한 객체면 에러 발생!!

- **해결책: **비교에 사용되지 않을 **고유한 카운터 값**을 튜플 중간에 넣어주기

    - `(priority, count, item)`

    - `count`는 삽입 순서대로 증가하는 정수.

    - 우선순위가 같을 경우, 먼저 삽입된 요소(count 가 작은)가 먼저 나오도록 보장 (안정성)

```python
import heapq
import itertools


# 우선순위와 데이터를 튜플로 묶어 사용하는 우선순위 큐
# (안정성을 위한 카운터 포함)
class PriorityQueue:
    def __init__(self):
        self.pq = []  # 리스트를 힙으로 사용
        self.counter = itertools.count()  # 삽입 순서 추적용 카운터

    def push(self, priority, item):
        # 음수 우선순위로 최대 힙처럼 동작
        # (값이 작을수록 우선순위 높음)
        count = next(self.counter)
        entry = (priority, count, item)
        heapq.heappush(self.pq, entry)

    def pop(self):
        if not self.pq:
            raise IndexError("pop from an empty priority queue")
        priority, count, item = heapq.heappop(self.pq)
        return item

    def peek(self):
        if not self.pq:
            raise IndexError("peek from an empty priority queue")
        priority, count, item = self.pq[0]
        return item

    def is_empty(self):
        return len(self.pq) == 0

    def __len__(self):
        return len(self.pq)


# 사용 예시
pq = PriorityQueue()
pq.push(3, "Task 3")
pq.push(1, "Task 1")
pq.push(2, "Task 2")
pq.push(1, "Task 1b")  # 같은 우선순위 다른 작업

while not pq.is_empty():
    print(pq.pop())
# 출력:
# Task 1 (우선순위 1인 첫 번째 항목)
# Task 1b (우선순위 1인 두 번째 항목)
# Task 2 (우선순위 2)
# Task 3 (우선순위 3)
```

## ⚡️ vs 🐢 성능 비교: 힙 vs 리스트 기반 우선순위 처리

### **시나리오**

많은 데이터 요소들을 우선순위에 따라 처리해야 하는 경우

- 예시) 가장 작은 값들을 반복적으로 찾아 제거

### 방법 1: 정렬되지 않은 리스트 사용

- 가장 작은 값 찾기: 매번 리스트 전체를 순회 (`min()` 또는 직접 비교) → **O(n)**

- 찾은 값 제거: `remove()` → **O(n)**

- k번 반복 시: **O(k*n)** (매우 비효율적)

### 방법 2: 정렬된 리스트 사용

- 처음에 정렬: `sort()` → **O(n log n)**

- 가장 작은 값 제거: `pop(0)` (리스트) → **O(n)** (뒤 요소들 이동) 또는 `pop()` (데크) O(1)

- 중간에 요소 추가: 정렬 위치 찾아 삽입 → **O(n)**

- 정렬 유지 비용이 큼

### 방법 3: 힙(`heapq`) 사용

- 힙 생성: `heapify()` → **O(n)**

- 가장 작은 값 제거: `heappop()` → **O(log n)**

- 요소 추가: `heappush()` → **O(log n)**

- k번 반복 시: 초기 힙 생성 O(n) + k번 pop O(k log n) → **O(n + k log n)** (훨씬 효율적!)

### 정렬과 리스트 사용 vs 힙 사용: 시간 복잡도 비교

- **정렬 + 리스트**: O(n log n) + O(k * n) = O(n log n + k * n)

- **힙**: O(n) + O(k log n) = O(n + k log n)

- 대개의 경우 `k`가 크면 힙이 훨씬 우수한 성능을 보임

### 결론

우선순위가 중요한 데이터를 **동적으로 추가/삭제**하면서 **지속적으로 가장 우선순위 높은 요소**를 찾아야 하는 경우, **힙(heapq)** 이 리스트 기반 방법보다 훨씬 뛰어난 성능을 제공한다!

## 💾💨 NumPy: 고성능 수치 계산을 위한 배열 구조

- 참고: [https://yuiyeong.github.io/posts/numpy/](https://yuiyeong.github.io/posts/numpy/)

### NumPy `ndarray` vs. 파이썬 `list`: 자료구조적 차이

데이터 과학에서 대규모 숫자 데이터를 다룰 때 파이썬 기본 리스트 대신 NumPy의 `ndarray` (N-dimensional array)를 사용하는 이유는 근본적인 자료구조 설계의 차이 때문입니다.

| 특징         | NumPy `ndarray`            | 파이썬 `list`                     | 
 |------------|----------------------------|--------------------------------| 
| **요소 타입**  | **동일 타입 (Homogeneous)**    | 다양한 타입 (Heterogeneous) 가능      | 
| **메모리 구조** | **연속된 메모리 블록** (데이터 직접 저장) | 각 요소의 **참조(주소)** 저장 (여기저기 흩어짐) | 
| **메모리 효율** | **높음** (타입 정보 오버헤드 없음)     | **낮음** (각 요소의 부가 정보 필요)        | 
| **연산 속도**  | **매우 빠름** (벡터화된 C 연산) ⚡️   | **느림** (파이썬 인터프리터 반복) 🐢       | 

**핵심:**

- **메모리 연속성 & 동일 타입**: `ndarray`는 같은 타입의 데이터를 메모리에 연속적으로 배치합니다. 이는 CPU 캐시 효율을 극대화하고, 각 요소의 타입을 확인할 필요 없이 데이터에 빠르게 접근하게
  해줍니다. 리스트는 각 요소의 메모리 주소를 저장하므로 데이터 접근 시 추가적인 간접 참조가 필요하고 캐시 효율이 떨어집니다.

- **벡터화 (Vectorization)**: NumPy는 내부적으로 C언어로 구현된 최적화된 반복문(ufuncs)을 통해 배열 전체에 대한 연산을 한 번에 처리합니다. 파이썬 레벨의 `for` 루프 없이 연산이
  가능해 매우 빠릅니다. 리스트는 파이썬 인터프리터를 통해 하나씩 요소를 처리해야 하므로 느립니다.

### `ndarray`의 기본 구조 속성

`ndarray` 객체는 자신의 구조를 나타내는 중요한 속성들을 가집니다.

- `ndarray.ndim`: 배열의 **차원 수** (축의 개수)

- `ndarray.shape`: 각 차원의 **크기(형태)** 를 튜플로 반환 (예: `(3, 4)`는 3행 4열)

- `ndarray.dtype`: 배열 요소의 **데이터 타입** (메모리 사용량과 연산 방식 결정. 매우 중요!)

```python
import numpy as np

# 리스트와 ndarray 비교
py_list = [1, 2, 3, 4, 5]
np_array = np.array(py_list)


# 메모리와 성능 차이 테스트
def square_list(lst):
    result = []
    for item in lst:
        result.append(item ** 2)
    return result


def square_array(arr):
    return arr ** 2  # 벡터화 연산, 훨씬 빠름!


# 간단한 비교
import time

# 큰 데이터 생성
big_list = list(range(1000000))
big_array = np.array(big_list)

# 리스트 제곱 시간 측정
start = time.time()
result_list = square_list(big_list)
list_time = time.time() - start

# NumPy 배열 제곱 시간 측정
start = time.time()
result_array = square_array(big_array)
array_time = time.time() - start

print(f"리스트 연산 시간: {list_time:.6f}초")
print(f"NumPy 배열 연산 시간: {array_time:.6f}초")
print(f"NumPy가 약 {list_time / array_time:.1f}배 빠름")

```

## 🐼🏷️ Pandas: 레이블 기반 데이터 분석 구조

- 참고: [https://yuiyeong.github.io/posts/pandas-marathon/](https://yuiyeong.github.io/posts/pandas-marathon/)

### Pandas 자료구조: NumPy 위에 구축된 레이블링

Pandas는 NumPy의 고성능 배열(`ndarray`)을 기반으로, 데이터 분석에 필수적인 **레이블(Label)** 기능을 추가한 자료구조를 제공합니다.

- `Series` (1차원):

    - 구조: **Index (레이블)** + **Values (NumPy 배열)**

    - NumPy 1차원 배열에 각 데이터 값(`Values`)을 식별할 수 있는 인덱스(`Index`) 레이블이 붙은 형태입니다. 인덱스는 단순 정수 위치뿐 아니라 문자열 등 사용자 정의가 가능합니다.

    - 마치 **레이블이 있는 NumPy 배열** 또는 **순서가 있는 딕셔너리**와 유사합니다.

- `DataFrame` (2차원):

    - 구조: **Index (행 레이블)** + **Columns (열 레이블)** + **Values (데이터, 내부적으로 NumPy 배열)**

    - NumPy 2차원 배열에 각 **행(row)** 을 식별하는 `Index` 레이블과 각 **열(column)** 을 식별하는 `Columns` 레이블이 추가된 형태입니다.

    - **각 열은 독립적인 `Series` 로 볼 수 있으며, **서로 다른 `dtype` 을 가질 수 있습니다. (NumPy 배열과의 주요 차이점)

    - 엑셀 스프레드시트나 SQL 테이블과 유사한 구조로, 정형 데이터를 다루는 데 최적화되어 있습니다.

### Series와 DataFrame 구조 확인

간단한 생성 예시를 통해 구조를 확인해 봅시다.

```python
import pandas as pd
import numpy as np

# Series 생성
s1 = pd.Series([10, 20, 30, 40])
print(s1)
# 출력:
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64

# 커스텀 인덱스를 가진 Series
s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s2)
# 출력:
# a    10
# b    20
# c    30
# d    40
# dtype: int64

# 딕셔너리로부터 Series 생성
s3 = pd.Series({'a': 10, 'b': 20, 'c': 30, 'd': 40})
# s2와 동일한 결과

# Series 구조 살펴보기
print("인덱스:", s2.index)  # Index(['a', 'b', 'c', 'd'], dtype='object')
print("값:", s2.values)  # array([10, 20, 30, 40])
print("데이터타입:", s2.dtype)  # int64

# DataFrame 생성
df1 = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Paris', 'London']
})
print(df1)
# 출력:
#       Name  Age      City
# 0    Alice   25  New York
# 1      Bob   30     Paris
# 2  Charlie   35    London

# DataFrame 구조 살펴보기
print("행 인덱스:", df1.index)  # RangeIndex(start=0, stop=3, step=1)
print("열 이름:", df1.columns)  # Index(['Name', 'Age', 'City'], dtype='object')
print("값:", df1.values)  # array([['Alice', 25, 'New York'], ...])
print("데이터타입:")
print(df1.dtypes)  # Name: object, Age: int64, City: object
```
