---
title: 😜 NumPy Cheat Sheet
date: 2025-04-01 12:26:00 +0900
categories:
  - PYTHON
  - NUMPY
tags:
  - 급발진거북이
  - python
  - numpy
  - GeekAndChill
  - 기깬칠
  - cheet_sheet
  - AI
  - 에이아이
toc: true
comments: false
mermaid: true
math: true
---

## 🗺️ 마인드맵

```shell
                        ┌── array() ── [1,2,3] → ndarray([1,2,3])
                        │
                        ├── zeros() ── shape=(2,3) → [[0,0,0],[0,0,0]]
                        │
              ┌─────────┼── ones() ─── shape=(2,3) → [[1,1,1],[1,1,1]]
              │         │
              │         ├── empty() ── shape=(2,3) → 초기화되지 않은 배열
    ┌─────────┤ 생성     │
    │         │         ├── arange() ─ start,stop,step → [0,1,2,3,4]
    │         │         │
    │         │         └── linspace() ─ start,stop,num → 균등 간격 분할
    │         │
    │         │         ┌── shape ─── 배열 크기 → (2,3)
    │         │         │
    │         └─────────┼── ndim ──── 차원 수 → 2
    │                   │
    │                   ├── dtype ─── 데이터 타입 → int64
    │                   │
    │                   └── size ──── 총 요소 수 → 6
    │
    │                   ┌── 기본 ─────── a[0,1] → 위치 [0,1]의 요소
    │                   │
    │                   ├── 슬라이싱 ─── a[0:2, 1:3] → 부분 배열
    ├───── 인덱싱 ────────┤
    │                   ├── 모든 행/열 ── a[:, 1] → 2번째 열 전체
    │                   │
    │                   ├── 팬시 ─────── a[[0,2], [1,3]] → 특정 위치
    │                   │
    │                   └── 불리언 ────── a[a > 5] → 조건 만족 요소
    │
    │                   ┌── +, -, *, / ─── 요소별 연산 → a+b, a*2
    │                   │
    │         ┌─────────┼── ** ──────────── 거듭제곱 → a**2
    │         │ 기본     │
    │         │         ├── @ ────────────── 행렬 곱셈 → a@b
    │         │         │
    │         │         ├── >, <, == ────── 비교 연산 → a>0
    │         │         │
    │         │         └── &, |, ~ ─────── 논리 연산 → (a>0) & (a<5)
    ├─────────┤
    │ 연산     │         ┌── sum() ──────── 합계 → np.sum(a, axis=0)
    │         │         │
    │         │         ├── min(), max() ── 최소/최대 → np.min(a)
    │         └─────────┤
    │           통계     ├── mean() ─────── 평균 → np.mean(a)
    │                   │
    │                   ├── argmin() ────── 최소값 인덱스 → np.argmin(a)
    │                   │
    │                   └── cumsum() ────── 누적합 → np.cumsum(a)
    │
    │                   ┌── reshape() ─── 모양 변경 → a.reshape(3,4)
    │                   │
    │                   ├── T ──────────── 전치 → a.T
    │                   │
    │         ┌─────────┼── ravel() ────── 1차원화 → a.ravel()
    │         │  변형    │
    ├─────────┤         └── resize() ───── 크기 변경 → a.resize((4,5))
    │         │
    │         │         ┌── vstack() ────── 수직 결합 → np.vstack((a,b))
    │         └─────────┤
    │           결합/분할 ├── hstack() ────── 수평 결합 → np.hstack((a,b))
    │                   │
    │                   ├── hsplit() ────── 수평 분할 → np.hsplit(a,3)
    │                   │
    │                   └── vsplit() ────── 수직 분할 → np.vsplit(a,2)
    │
    │                   ┌── sqrt() ───────── 제곱근 → np.sqrt(a)
    │                   │
    │                   ├── exp(), log() ─── 지수/로그 → np.exp(a)
    └────── 수학 ────────┤
                        ├── sin(), cos() ─── 삼각함수 → np.sin(a)
                        │
                        ├── floor(), ceil() ─ 내림/올림 → np.floor(a)
                        │
                        └── round() ──────── 반올림 → np.round(a,2)

```

## 💯 핵심 개념

### Broadcasting

서로 다른 크기의 배열 간 연산 자동 확장

```python
a = np.array([1, 2, 3])  # (3,)
b = np.array([[1], [2], [3]])  # (3,1)
c = a + b  # (3,3)
```

### View vs Copy

```python
a = np.array([1, 2, 3, 4])
b = a[1:3]  # 뷰 - a 변경 시 b도 변경
c = a[1:3].copy()  # 복사 - 독립적 객체
```

### axis 파라미터

```plain text
axis=0: 행 방향 연산 (열을 따라 아래로)
axis=1: 열 방향 연산 (행을 따라 오른쪽으로)
```

### dtype 옵션

```plain text
int32, int64, float32, float64, bool, complex
```

## 🔨 배열 생성

```python
# 기본 배열 생성
a = np.array([1, 2, 3])  # [1 2 3]
b = np.array([[1, 2], [3, 4]])  # [[1 2]
#  [3 4]]

# 특수 배열
np.zeros((2, 3))  # [[0. 0. 0.]
#  [0. 0. 0.]]
np.ones((2, 2))  # [[1. 1.]
#  [1. 1.]]
np.empty((2, 2))  # 초기화 안된 값
np.eye(3)  # 3x3 단위행렬
np.identity(3)  # 3x3 단위행렬

# 범위 배열
np.arange(5)  # [0 1 2 3 4]
np.arange(1, 6, 2)  # [1 3 5]
np.linspace(0, 1, 5)  # [0.   0.25 0.5  0.75 1.  ]

```

## 📊 배열 속성

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

a.shape  # (2, 3)
a.ndim  # 2
a.dtype  # int64
a.size  # 6
a.itemsize  # 8 bytes

```

## 🔍 인덱싱 & 슬라이싱

```python
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# 기본 인덱싱
a[0, 0]  # 1
a[2, 3]  # 12

# 슬라이싱
a[0:2, 1:3]  # [[2 3]
#  [6 7]]
a[:, 1]  # [2 6 10]
a[1, :]  # [5 6 7 8]

# 팬시 인덱싱
a[[0, 2], [1, 3]]  # [2 12]
a[[0, 2]]  # [[1 2 3 4]
#  [9 10 11 12]]

# 불리언 인덱싱
mask = a > 5
a[mask]  # [6 7 8 9 10 11 12]
a[a > 5]  # [6 7 8 9 10 11 12]
a[(a > 5) & (a < 10)]  # [6 7 8 9]

```

## 🔢 연산

```python
a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])

# 기본 연산
a + b  # [11 22 33 44]
a - b  # [9 18 27 36]
a * b  # [10 40 90 160]
a / b  # [10. 10. 10. 10.]
a ** 2  # [100 400 900 1600]
a % 3  # [1 2 0 1]
a // 3  # [3 6 10 13]

# 행렬 곱셈
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
A @ B  # [[19 22]
#  [43 50]]
np.dot(A, B)  # 동일한 결과

# 비교 연산
a > 25  # [False False True True]
a == 30  # [False False True False]
np.array_equal(a, b)  # False

# 논리 연산
(a > 20) & (a < 40)  # [False False True False]
(a <= 20) | (a >= 40)  # [True True False True]
~(a > 30)  # [True True True False]

```

## 📈 통계 함수

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

# 기본 통계
np.sum(a)  # 21
np.sum(a, axis=0)  # [5 7 9]
np.sum(a, axis=1)  # [6 15]

np.min(a)  # 1
np.max(a)  # 6
np.mean(a)  # 3.5
np.median(a)  # 3.5
np.std(a)  # 1.707...

# 인덱스 관련
np.argmin(a)  # 0
np.argmax(a)  # 5
np.argmin(a, axis=0)  # [0 0 0]
np.argmax(a, axis=1)  # [2 2]

# 누적 함수
np.cumsum(a)  # [1 3 6 10 15 21]
np.cumprod(a)  # [1 2 6 24 120 720]

```

## 🔄 형태 변환

```python
a = np.arange(12)

# 형태 변환
a.reshape(3, 4)  # 3x4 배열
a.reshape(3, -1)  # 열 자동 계산
a.reshape(-1, 2)  # 행 자동 계산
a.ravel()  # 1차원 평탄화 [0 1 2 ... 11]

# 전치 (Transpose)
b = a.reshape(3, 4)
b.T  # 4x3 전치 행렬

# 크기 변경
# (a의 크기가 실제로 변경됨)
a.resize(3, 4)

```

## 🔗 결합 & 분할

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# 결합
np.vstack((a, b))  # [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

np.hstack((a, b))  # [[1 2 5 6]
#  [3 4 7 8]]

np.concatenate((a, b), axis=0)  # vstack와 동일
np.concatenate((a, b), axis=1)  # hstack와 동일

# 분할
a = np.arange(16).reshape(4, 4)
np.hsplit(a, 2)  # [array([[0, 1], [4, 5], [8, 9], [12, 13]]),
#  array([[2, 3], [6, 7], [10, 11], [14, 15]])]

np.vsplit(a, 2)  # [array([[0, 1, 2, 3], [4, 5, 6, 7]]),
#  array([[8, 9, 10, 11], [12, 13, 14, 15]])]

np.split(a, 2, axis=0)  # vsplit와 동일
np.split(a, 2, axis=1)  # hsplit와 동일

```

## 🧮 수학 함수

```python
a = np.array([0, np.pi / 2, np.pi])

# 기본 함수
np.sqrt(a)  # [0. 1.25331414 1.77245385]
np.exp(a)  # [1. 4.81047738 23.14069263]
np.log(np.array([1, 10, 100]))  # [0. 2.30258509 4.60517019]
np.log10(np.array([1, 10, 100]))  # [0. 1. 2.]

# 삼각 함수
np.sin(a)  # [0. 1. 0.]
np.cos(a)  # [1. 0. -1.]
np.tan(a)  # [0. 16331239353195370. 0.]
np.degrees(a)  # [0. 90. 180.]
np.radians(np.array([0, 90, 180]))  # [0. 1.57079633 3.14159265]

# 반올림 함수
np.floor(np.array([1.2, 1.5, 1.8, 2.1]))  # [1. 1. 1. 2.]
np.ceil(np.array([1.2, 1.5, 1.8, 2.1]))  # [2. 2. 2. 3.]
np.round(np.array([1.2, 1.5, 1.8, 2.1]))  # [1. 2. 2. 2.]
np.round(np.array([1.23, 1.56]), 1)  # [1.2 1.6]

```

## 🏷️ View vs Copy

```python
a = np.array([1, 2, 3, 4])

# View (데이터 공유)
b = a[1:3]  # [2 3]
b[0] = 99  # b는 이제 [99 3]
print(a)  # [1 99 3 4] (a도 변경됨)

# Copy (독립적 객체)
c = a[1:3].copy()  # [99 3]
c[0] = 88  # c는 이제 [88 3]
print(a)  # [1 99 3 4] (a는 변경 안됨)

```

## 📡 Broadcasting

```python
# 스칼라와 배열
a = np.array([1, 2, 3])
b = a * 2  # [2 4 6]

# 다른 형태 배열 간 연산
a = np.array([1, 2, 3])  # (3,) 형태
b = np.array([[1], [2], [3]])  # (3,1) 형태
c = a + b  # (3,3) 형태의 결과:
# [[2 3 4]
#  [3 4 5]
#  [4 5 6]]

```

## 🧩 유용한 함수

```python
# 배열 정보
np.info(np.ndarray)  # ndarray 클래스 정보 출력

# 난수 생성
np.random.rand(2, 3)  # 2x3 균등분포 난수 (0~1)
np.random.randn(2, 3)  # 2x3 표준정규분포 난수
np.random.randint(1, 10, (2, 3))  # 1~9 범위의 2x3 정수 난수

# 정렬
a = np.array([3, 1, 2])
np.sort(a)  # [1 2 3]
a.sort()  # a 자체를 정렬

# 고유값
np.unique(np.array([1, 2, 2, 3, 3, 3]))  # [1 2 3]

# 차원 추가/제거
a = np.array([1, 2, 3])
a[:, np.newaxis]  # 열 벡터로 변환 [[1], [2], [3]]
a = np.array([[1], [2], [3]])
a.squeeze()  # 1차원으로 변환 [1 2 3]

```

